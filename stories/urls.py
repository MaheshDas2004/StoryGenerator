from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('createstory/',views.createstory,name="create_story"),
    path("viewstory/", views.viewstory, name="view_story"),
    path("viewstory/<int:story_id>/", views.viewstory, name="view_saved_story"),
    path("savestory/", views.savestory, name="save_story"),

]