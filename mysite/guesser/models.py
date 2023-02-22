from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re


class Video(models.Model):
    ign = models.CharField(max_length=200, verbose_name="In-Game Name")
    url = models.URLField(validators=[URLValidator()])
    rank = models.CharField(max_length=20)

    def clean(self):
        youtube_regex = r'^https:\/\/(www\.)?youtube\.com\/watch\?v=[a-zA-Z0-9_-]{11}$'
        youtube_url = self.url
        if not re.match(youtube_regex, youtube_url):
            raise ValidationError('Invalid YouTube URL')

    def __str__(self):
        return f"{self.rank} - {self.ign}"

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'


class Guess(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    guess = models.CharField(max_length=20)
    is_correct = models.BooleanField()

    class Meta:
        verbose_name = 'Guess'
        verbose_name_plural = 'Guesses'
