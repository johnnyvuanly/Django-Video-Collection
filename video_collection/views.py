from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower
from .forms import VideoForm, SearchForm
from .models import Video # Video model describes the structure of the database and it describes the structure of the object in your code

# Create your views here.
def home(request):
    app_name = 'Coding Videos'
    return render(request, 'video_collection/home.html', {'app_name': app_name})

def add(request):

    if request.method == 'POST':
        # Equal to video form the class created from the data that was sent to the server 
        new_video_form = VideoForm(request.POST)
        if new_video_form.is_valid():
            try:
                new_video_form.save()
                return redirect('video_list')
                # messages.info(request, 'New video saved!')
            # TODO show success message or redirect to list of videos
            except ValidationError:
                messages.warning(request, 'Invalid YouTube URL')
            except IntegrityError: # Caused by a duplicate video
                messages.warning(request, 'You already added that video')
        
        messages.warning(request, 'Please check the data entered')
        return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

def video_list(request):

    search_form = SearchForm(request.GET) # Build form from data user has sent to app

    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term'] # example: 'Vue' or 'tutorial'
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name')) # name__icontains is a Django query
    else: # form is not filled in or this the first time the user sees the page
        search_form = SearchForm()
        videos = Video.objects.order_by(Lower('name')) # Lower will convert video titles to lowercase order and then return the correct case

    return render(request, 'video_collection/video_list.html', {'videos': videos, 'search_form': search_form}) # Quick tip you do not have to have the same name for your templates and your functions and URLs