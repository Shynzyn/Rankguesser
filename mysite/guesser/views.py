from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import VideoUploadForm

from django.utils import timezone
from .models import Video, Guess

import random

def index(request):
    return HttpResponse("Hello World")


def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = VideoUploadForm()
    return render(request, 'upload_video.html', {'form': form})


def video_guess(request):
    # Get a random video from the database
    video = random.choice(Video.objects.all())

    # If the visitor has submitted a guess
    if request.method == 'POST':
        guess = request.POST['guess']
        is_correct = (guess == video.rank)

        # Create a new Guess object and save it to the database
        guess_obj = Guess(video=video, guess=guess, is_correct=is_correct)
        guess_obj.save()

        # Render a response that shows the result of the guess
        return render(request, 'video_guess_result.html', {
            'video': video,
            'guess': guess,
            'is_correct': is_correct,
        })

    # If the visitor hasn't submitted a guess yet
    else:
        # Render the template with the random video
        return render(request, 'video_guess.html', {'video': video})