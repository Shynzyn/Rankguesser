from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_video, name='upload'),
    path('guess/', views.video_guess, name='guess'),
    path('register', views.register, name='register'),
    path('already_guessed', views.already_guessed, name='already_guessed'),
    path('no_videos_left', views.no_videos_left, name='no_videos_left'),
    path('profile_update', views.profile_update, name='profile_update'),
    path('profile', views.profile, name='profile'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]