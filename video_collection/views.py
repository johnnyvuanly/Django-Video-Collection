from django.shortcuts import render
from .models import Video
from .forms import VideoForm
from django.contrib import messages

# Create your views here.
def home(request):
    app_name = 'Coding Videos'
    return render(request, 'video_collection/home.html', {'app_name': app_name})

def add(request):

    if request.method == 'POST':
        # Equal to video form the class created from the data that was sent to the server 
        new_video_form = VideoForm(request.POST)
        if new_video_form.is_valid():
            new_video_form.save()
            messages.info(request, 'New video saved!')
            # TODO show success message or redirect to list of videos
        else:
            messages.warning(request, 'Please check the data entered')
            return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

