from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Categories, Comment, Genres, Review, Titles

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class EmailAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=100)

    def validate(self, data):
        user = get_object_or_404(
            User, confirmation_code=data['confirmation_code'],
            email=data['email']
        )
        return get_tokens_for_user(user)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'role', 'email', )
        model = User


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        model = Genres


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        model = Categories


class CustomField(serializers.SlugRelatedField):

    def to_representation(self, obj):
        return {'name': obj.name, 'slug': obj.slug}


class TitlesSerializer(serializers.ModelSerializer):
    genre = CustomField(
        slug_field='slug',
        many=True,
        queryset=Genres.objects.all()
    )

    category = CustomField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    rating = serializers.SerializerMethodField('get_rating')

    def get_rating(self, title):
        rating = Review.objects.filter(title=title.id).\
            aggregate(average_score=Avg('score'))

        return rating['average_score'] or None

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Titles


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context['request'].path.split('/')[4]
            if Review.objects.filter(author=user, title__id=title_id).exists():
                raise serializers.ValidationError("Вы уже оставили отзыв на данное произведение")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
