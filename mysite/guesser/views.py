from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import gettext as _
from django.contrib import messages
from .forms import VideoUploadForm, UserUpdateForm, ProfileUpdateForm
from .models import Video, Guess, Profile
from django.views.generic import ListView
import random


def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('index')


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
        'iron': {
            'url': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/1.png',
            'color': '#7b6c6a',
        },
        'bronze': {
            'url': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/2.png',
            'color': '#9e7061',
        },
        'silver': {
            'url': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/3.png',
            'color': '#84929d',
        },
        'gold': {
            'url': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/4.png',
            'color': '#c5965c',
        },
        'platinum': {
            'url': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/5.png',
            'color': '#41977e',
        },
        'diamond': {
            'url': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/6.png',
            'color': '#365ab8',
        },
        'master': {
            'url': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/7.png',
            'color': '#d36efb',
        },
        'grandmaster': {
            'url': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/8.png',
            'color': '#d25629',
        },
        'challenger': {
            'url': 'https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/9.png',
            'color': '#5dabb5',
        },
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
        profile = Profile.objects.get(user=request.user)
        if is_correct:
            profile.exp_points += 80
            profile.save()
            if profile.exp_points >= profile.experience_needed:
                profile.level += 1
                profile.exp_points = profile.exp_points - profile.experience_needed
                profile.experience_needed = profile.experience_needed * 1.1
                profile.save()
                profile.update_rank()

        guess_count = Guess.objects.filter(video=video, guess=guess).count()
        total_guesses = Guess.objects.filter(video=video).count()
        rank_count = {}

        for rank in ranks_dict.keys():
            count = Guess.objects.filter(video=video, guess=rank).count()
            if count > 0:
                percentage = round(count / total_guesses * 100, 1)
                rank_count[rank] = {
                    'percentage': percentage,
                    'url': ranks_dict[rank]['url'],
                    'color': ranks_dict[rank]['color']
                }

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


@login_required
def profile_update(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile has been updated.")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile_update.html', context)


def profile(request):
    profile = Profile.objects.get(user=request.user)
    progress = profile.exp_points / profile.experience_needed * 100
    context = {
        'progress': progress,
        'profile': profile,
    }
    return render(request, 'profile.html', context)


def leaderboard(request):
    profiles = Profile.objects.order_by('-level', '-exp_points')
    paginator = Paginator(profiles, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'leaderboard.html', {'page_obj': page_obj})
