from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Title(models.Model):
    pass


class Review(models.Model):

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(),
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )
# первый вариант реализации score
# SCORE_CHOICES = zip(range(1, 11), range(1, 11))
# score = models.IntegerField(choices=SCORE_CHOICES)

# второй вариант реализации score
# from django.core.validators import MinValueValidator, MaxValueValidator
# score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
        db_index=True
    )
