from django.shortcuts import render,redirect
from django.contrib.auth.models import User 
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_protect, csrf_exempt

# "error_email": "Email already exists",
#             "error_password": "Passwords do not match",
#             "error_confirm_password": "Please confirm your password",
# Create your views here.

def create_story(request):
    genres = [
        ('fantasy', 'Fantasy'),
        ('adventure', 'Adventure'),
        ('mystery', 'Mystery'),
        ('sci-fi', 'Sci-Fi'),
        ('funny', 'Funny'),
    ]
    settings = ['castle', 'space', 'jungle', 'ocean', 'desert']
    age_options = ['5-7', '8-10', '11-13']

    if request.method == 'POST':
        # Handle form submission
        pass

    return render(request, 'stories/createstory.html', {
        'genres': genres,
        'settings': settings,
        'age_options': age_options,
    })


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
        
def logout_user(request):
    logout(request)
    return redirect("home")

def login_user(request):
    context={}
    if request.GET.get("forgetpass"):
        params={}
        params["showModal"]=True
        return render(request,"accounts/login.html",params)
    
    if request.method=="POST":
        verifyUser=request.POST.get("verify_user")
        if verifyUser:
            email=request.POST.get("email")
            # print(email)
            try:
                user=User.objects.get(username=email)
                if user:
                    context["showReset"]=True                    
                    context["email"]=email                    
            except User.DoesNotExist:
                context["error_email"]="Incorrect email,Email does not exist"
                context["showModal"]=True
            return render(request,"accounts/login.html",context)
        
        elif request.POST.get("reset_password"):
            email=request.POST.get("email")
            new_password=request.POST.get("new_password")
            cfpassword=request.POST.get("confirm_newpassword")
            # print(new_password+" "+cfpassword)
            if new_password != cfpassword:
                context["error_password"]="Passwords do not match"
                context["showReset"]=True
                context["email"]=email
                return render(request,"accounts/login.html",context)
            try:
                user = User.objects.get(username=email)
                user.set_password(new_password)
                user.save()
                context["success"] = "Password updated successfully!"
            except User.DoesNotExist:
                context["error_email"] = "User not found"
            return render(request, "accounts/login.html", context)


        else:
            email=request.POST.get("email")
            password=request.POST.get("password")
            context={}
            try:
                User.objects.get(username=email)
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
