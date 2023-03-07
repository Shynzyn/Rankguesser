from django import forms
from django.contrib.auth.models import User

from .models import Video
import re


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['url', 'ign', 'champion', 'rank']

    def clean_youtube_url(self):
        youtube_url = self.cleaned_data['youtube_url']
        if not is_valid_youtube_url(youtube_url):
            raise forms.ValidationError("Please enter a valid YouTube URL.")
        return youtube_url


def is_valid_youtube_url(url):
    regex = r'^https:\/\/(www\.)?youtube\.com\/watch\?v=[a-zA-Z0-9_-]{11}$'
    return bool(re.match(regex, url))


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
