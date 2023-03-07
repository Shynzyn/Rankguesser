from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re


class Video(models.Model):
    ign = models.CharField(max_length=200, verbose_name="In-Game Name")
    url = models.URLField(validators=[URLValidator()])
    champion = models.CharField(max_length=30, verbose_name="Champion", null=True)
    rank_choices = [
        ('iron', 'Iron'),
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('diamond', 'Diamond'),
        ('master', 'Master'),
        ('grandmaster', 'Grandmaster'),
        ('challenger', 'Challenger'),
    ]
    rank = models.CharField(max_length=30, choices=rank_choices)


    def __str__(self):
        return f"{self.rank} - {self.ign}"

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'


def clean(self):
    youtube_regex = r'^https:\/\/(www\.)?youtube\.com\/watch\?v=[a-zA-Z0-9_-]{11}$'
    youtube_url = self.url
    if not re.match(youtube_regex, youtube_url):
        raise ValidationError('Invalid YouTube URL')


class Guess(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    guess = models.CharField(max_length=20)
    is_correct = models.BooleanField()
    date_guessed = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'video')
        verbose_name = 'Guess'
        verbose_name_plural = 'Guesses'

    def __str__(self):
        return f"{self.user}, video: {self.video}, guess: {self.guess}, date: {self.date_guessed}"
