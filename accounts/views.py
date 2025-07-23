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
        
def login_user(request):
    if request.method=="POST":
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
def logout_user(request):
    logout(request)
    return redirect("home")

@csrf_protect
def forgot_password(request):
    if request.method == 'POST':
        # full_name = request.POST.get('full_name')
        email = request.POST.get('email')

        # if not full_name or not email:
        #     messages.error(request, "Please fill in all fields.")
        #     return redirect('login')
        
        if  not email:
            messages.error(request, "Please fill in all fields.")
            return redirect('login')

        # try:
        #     first_name, last_name = full_name.strip().split(' ', 1)
        # except ValueError:
        #     messages.error(request, "Please enter both first and last name.")
        #     return redirect('login')

        user = User.objects.filter( email=email).first()

        if user:
            # Store temporary user info in session
            request.session['reset_user_id'] = user.id
            return redirect('reset_password')  # Next page for password reset
        else:
            messages.error(request, "No user found with the given details.")
            return redirect('login')
        
@csrf_protect
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not (email and new_password and confirm_password):
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'})

        if new_password != confirm_password:
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match.'})

        user = User.objects.filter(email=email).first()

        if not user:
            return JsonResponse({'status': 'error', 'message': 'User not found.'})

        user.password = make_password(new_password)
        user.save()

        return JsonResponse({'status': 'success', 'message': 'Password reset successful.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def verify_user(request):
    if request.method == "POST":
        # full_name = request.POST.get("full_name")
        email = request.POST.get("email")

        try:
            # user = User.objects.get(email=email, first_name=full_name)
            user = User.objects.get(email=email)
            return JsonResponse({'status': 'success', 'email': email})
        except User.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'User not found'})