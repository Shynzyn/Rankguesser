from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import gettext as _
from django.contrib import messages
from .forms import VideoUploadForm
from .models import Video, Guess

import random


def index(request):
    return render(request, 'index.html')


def already_guessed(request):
    return render(request, 'you_already_guessed.html')


def no_videos_left(request):
    return render(request, 'no_videos_left.html')


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


@login_required
def video_guess(request):
    global video

    ranks_dict = {
        'iron': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/1.png',
        'bronze': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/2.png',
        'silver': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/3.png',
        'gold': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/4.png',
        'platinum': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/5.png',
        'diamond': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/6.png',
        'master': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/7.png',
        'grandmaster': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/8.png',
        'challenger': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/9.png',
    }

    user = request.user
    guessed_videos = Guess.objects.filter(user=user).values_list('video__id', flat=True)
    videos = Video.objects.exclude(id__in=guessed_videos)
    if not videos.exists():
        messages.error(request, 'You have already guessed all the videos.')
        return redirect('no_videos_left')

    # If the visitor has submitted a guess
    if request.method == 'POST':
        guess = request.POST.get('guess')
        is_correct = guess == video.rank

        if Guess.objects.filter(user=user, video=video).exists():
            messages.error(request, 'You have already guessed for this video.')
            return redirect('already_guessed')

        guess_obj = Guess(video=video, guess=guess, is_correct=is_correct, user=user)
        guess_obj.save()
        guess_count = Guess.objects.filter(video=video, guess=guess).count()
        total_guesses = Guess.objects.filter(video=video).count()
        rank_count = {}

        for rank in ranks_dict:
            count = Guess.objects.filter(video=video, guess=rank).count()
            rank_count[rank] = count

        return render(request, 'video_guess_result.html', {
            'video': video,
            'guess': guess,
            'is_correct': is_correct,
            'rank_link': ranks_dict[video.rank],
            'guess_link': ranks_dict[guess],
            'guess_count': guess_count,
            'total_guesses': total_guesses,
            'rank_count': rank_count,
        })
    else:
        video = random.choice(videos)

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
