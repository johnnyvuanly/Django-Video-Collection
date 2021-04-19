# This will be the urls for our app. Each page needs a URL, View, Template
from django.urls import path
from . import views

urlpatterns = [
    # Call the function in called home in views.py
    path('', views.home, name='home'),
    path('add', views.add, name='add_video')
]