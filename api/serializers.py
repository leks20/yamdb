from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers

from .models import Categories, Genres, Titles, Comment, Review

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'role', 'email',)
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

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
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
