from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAdmin, IsModerator, IsUser
from api.serializers import UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    print(queryset)
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
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
