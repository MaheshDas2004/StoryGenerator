from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from stories.models import Story

# Create your views here.
def home(request):
    return render(request,"home/home.html")
def about(request):
    return render(request, "home/about.html")
@login_required
def dashboard(request):
    story=Story.objects.filter(user=request.user)
    return render(request,"home/dashboard.html",{"user_stories":story})

    