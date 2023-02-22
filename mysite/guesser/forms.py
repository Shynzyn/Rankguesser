from django import forms
from .models import Video
import re


class VideoUploadForm(forms.ModelForm):
    url = forms.URLField(label='YouTube URL', max_length=200)
    ign = forms.CharField(label='In-Game Name', max_length=50)
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
    rank = forms.ChoiceField(choices=rank_choices)

    class Meta:
        model = Video
        fields = ['url', 'ign', 'rank']

    def clean_youtube_url(self):
        youtube_url = self.cleaned_data['youtube_url']
        if not is_valid_youtube_url(youtube_url):
            raise forms.ValidationError("Please enter a valid YouTube URL.")
        return youtube_url


def is_valid_youtube_url(url):
    regex = r'^https:\/\/(www\.)?youtube\.com\/watch\?v=[a-zA-Z0-9_-]{11}$'
    return bool(re.match(regex, url))
