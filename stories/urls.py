from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('createstory/',views.createstory,name="create_story"),
]