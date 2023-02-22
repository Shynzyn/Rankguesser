from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import VideoUploadForm


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
