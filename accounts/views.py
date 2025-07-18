from django.shortcuts import render

# Create your views here.
def signup(request):
    if request.method=="POST":
        username=request.POST.get
    return render(request,"accounts/signup.html")
def login(request):
    if request.method=="POST":
        username=request.POST.get
    return render(request,"accounts/login.html")