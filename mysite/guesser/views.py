from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import gettext as _
from django.contrib import messages
from .forms import VideoUploadForm

from django.utils import timezone
from .models import Video, Guess

import random


def index(request):
    return render(request, 'index.html')


def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = VideoUploadForm()
    return render(request, 'upload_video.html', {'form': form})


video = False


def video_guess(request):
    global video
    # Get a random video from the database

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
        video = random.choice(Video.objects.all())
        return render(request, 'video_guess.html', {'video': video})


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, _('Username %s already exists!') % username)
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, _('Email "%s" is already in use') % email)
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, _('User %s successfully created!') % username)
                    return redirect('login')
        else:
            messages.error(request, _("Password don't match!"))
            return redirect('register')
    return render(request, 'register.html')
