from django.shortcuts import render,redirect
from django.contrib.auth.models import User 
from django.contrib.auth import login,logout,authenticate
# "error_email": "Email already exists",
#             "error_password": "Passwords do not match",
#             "error_confirm_password": "Please confirm your password",
# Create your views here.
def signup(request):
    if request.method=="POST":
        firstname=request.POST.get("first_name")
        lastname=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("email")
        password=request.POST.get("password")
        cfpassword=request.POST.get("confirm_password")
        context = {}
        if password != cfpassword:
            context["error_password"]="Passwords do not match"    
            context["error_confirm_password"]="Passwords do not match"    
            return render(request,"accounts/signup.html",context)
        
        if User.objects.filter(username=email).exists():
            context["error_email"]="Email already exists"
            return render(request,"accounts/signup.html",context)
        
        if len(password)<6:
            context["error_password"]="password length must be atleast 6 characters"    
            return render(request,"accounts/signup.html",context)

        user=User.objects.create_user(username=username, email=email,password=password,first_name=firstname,last_name=lastname)
        login(request,user)
        return redirect("home")           



    return render(request,"accounts/signup.html")
        
def login_user(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        context={}
        try:
            user_exist=User.objects.get(username=email)
        except User.DoesNotExist:
            context["error_email"]="Email does not exist create one"
            return render(request,"accounts/login.html",context)


        user= authenticate(request, username=email, password=password)
        if(user):
            login(request,user)
            return redirect("home")
        else:
            context["error_password"]="Invalid Password!"
            return render(request,"accounts/login.html",context)

    return render(request,"accounts/login.html")
def logout_user(request):
    logout(request)
    return redirect("home")