from rest_framework import serializers

from .models import Categories, Genres, Titles


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Genres


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
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
