from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .permissions import IsAdmin, IsModerator, IsUser, IsAdminUserOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from .filters import TitlesFilter
from .models import Categories, Genres, Review, Titles, Comment
from .permissions import IsAdmin, IsModerator, IsUser, IsOwner
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, ReviewSerializer, TitlesSerializer,
                          UserSerializer)

User = get_user_model()


class GenresViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [IsAdminUserOrReadOnly, ]
    lookup_field = 'slug'
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', ]


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [IsAdminUserOrReadOnly, ]
    lookup_field = 'slug'
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', ]


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[IsAuthenticated],
            url_path='me', url_name='me')
    def me(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
        return Response(serializer.data)


class Auth():

    def email_is_valid(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def confirmation_code_generator(email, timestamp):
        pass

    @api_view(['POST'])
    @permission_classes([AllowAny])
    def send_confirmation_code(request):
        email = request.data.get('email')
        if email is None:
            return print('email required')
        else:
            content = {}
        if Auth.email_is_valid(email):
            content = {'status': email}
        return Response(content)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwner]
    permission_classes_by_action = {'list': [AllowAny],
                                    'create': [IsUser | IsAdmin | IsModerator],
                                    'retrieve': [AllowAny],
                                    'partial_update': [IsOwner],
                                    'destroy': [IsAdmin | IsModerator]}

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        queryset = Review.objects.filter(title__id=self.kwargs.get('title_id'))
        return queryset

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwner]
    permission_classes_by_action = {'list': [AllowAny],
                                    'create': [IsUser | IsAdmin | IsModerator],
                                    'retrieve': [AllowAny],
                                    'partial_update': [IsOwner],
                                    'destroy': [IsModerator | IsAdmin]}

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        queryset = Comment.objects.filter(review__id=self.kwargs.get('review_id'))
        return queryset

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
