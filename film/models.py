from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from accounts.models import CustomUser
from django.db.models import Sum


# Create your models here.


class Film(models.Model):
    name = models.CharField(max_length=250)
    year = models.CharField(max_length=250)
    genre = models.CharField(max_length=250)
    # like_count = models.PositiveIntegerField()

    @property
    def number_of_likes(self):
        return Like.objects.filter(film=self).count()

    @property
    def score_amounts(self):
        return Score.objects.filter(film=self).aggregate(score=Sum("score"))["score"]

    def __str__(self):
        return f"{self.name}"


class Like(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    film = models.ForeignKey(Film, on_delete=models.PROTECT)
    liked_at = models.DateTimeField(auto_now=True)


class Score(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    film = models.ForeignKey(Film, on_delete=models.PROTECT)
    score = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],null=True)
    scored_at = models.DateTimeField(auto_now=True)



class Critique(models.Model):
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_sploiler = models.BooleanField(default=False)
    content = models.TextField()
    writer = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
