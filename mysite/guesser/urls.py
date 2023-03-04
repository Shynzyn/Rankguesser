from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_video, name='upload'),
    path('guess/', views.video_guess, name='guess'),
    path('register', views.register, name='register'),
]