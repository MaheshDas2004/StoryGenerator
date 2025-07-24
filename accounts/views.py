from django.shortcuts import render,redirect
from django.contrib.auth.models import User 
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# "error_email": "Email already exists",
#             "error_password": "Passwords do not match",
#             "error_confirm_password": "Please confirm your password",
# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse
import json

def create_story(request):
    age_ranges = ["5-7", "8-10", "11-13"]
    
    genres = [
        ("fantasy", "🧚"), ("adventure", "🏞️"), ("sci-fi", "👽"),
        ("mystery", "🕵️"), ("funny", "😂"), ("educational", "📘")
    ]
    
    settings = [
        ("magical-forest", "🌲", "Magical forest"),
        ("enchanted-castle", "🏰", "Enchanted castle"),
        ("underwater-kingdom", "🌊", "Underwater kingdom"),
        ("space-station", "🛸", "Space station"),
        ("haunted-mansion", "🏚️", "Haunted mansion")
    ]
    
    lengths = [
        ("short", "Short (5-10 mins)"),
        ("medium", "Medium (10-15 mins)"),
        ("long", "Long (15-20 mins)")
    ]
    
    special_elements = [
        ("talking-animals", "🐾", "Talking animals"),
        ("magic-powers", "⚡", "Magic powers"),
        ("treasure-hunt", "💎", "Treasure hunt"),
        ("time-travel", "⏰", "Time travel"),
        ("dragons", "🐉", "Dragons"),
        ("robots", "🤖", "Robots")
    ]
    
    story = None
    
    if request.method == 'POST':
        # Get form data
        character_name = request.POST.get('characterName', '')
        age = request.POST.get('age', '')
        selected_genres = request.POST.getlist('genre')
        setting = request.POST.get('setting', '')
        length = request.POST.get('length', '')
        selected_elements = request.POST.getlist('elements')
        additional_notes = request.POST.get('additionalNotes', '')
        
        # Here you would typically call your AI story generation function
        # For now, we'll create a sample story based on the inputs
        story = generate_story(
            character_name, age, selected_genres, setting, 
            length, selected_elements, additional_notes
        )
    
    return render(request, "stories/createstory.html", {
        "age_ranges": age_ranges,
        "genres": genres,
        "settings": settings,
        "lengths": lengths,
        "special_elements": special_elements,
        "story": story
    })

def generate_story(character_name, age, genres, setting, length, elements, notes):
    """
    This is a placeholder function for story generation.
    Replace this with your actual AI story generation logic.
    """
    
    # Sample story generation based on inputs
    if not character_name:
        character_name = "Alex"
    
    setting_map = {
        "magical-forest": "a mystical forest filled with ancient trees and magical creatures",
        "enchanted-castle": "a grand castle where magic flows through every stone",
        "underwater-kingdom": "a beautiful kingdom beneath the ocean waves",
        "space-station": "a high-tech space station orbiting a distant planet",
        "haunted-mansion": "a mysterious mansion with secrets in every room"
    }
    
    setting_description = setting_map.get(setting, "a wonderful place")
    
    # Create a basic story structure
    story_parts = []
    
    # Opening
    story_parts.append(f"Once upon a time, there lived a brave young hero named {character_name}.")
    story_parts.append(f"One day, {character_name} discovered {setting_description}.")
    
    # Add elements based on selected special elements
    if "magic-powers" in elements:
        story_parts.append(f"{character_name} suddenly felt a tingling sensation and realized they had magical powers!")
    
    if "talking-animals" in elements:
        story_parts.append(f"To their surprise, {character_name} met a wise talking animal who became their guide.")
    
    if "treasure-hunt" in elements:
        story_parts.append(f"The animal told {character_name} about a legendary treasure hidden somewhere nearby.")
    
    if "dragons" in elements:
        story_parts.append(f"But beware! A mighty dragon guards the treasure, and only the pure of heart can pass.")
    
    # Adventure based on genre
    if "adventure" in genres:
        story_parts.append(f"{character_name} embarked on an exciting journey, facing challenges with courage and determination.")
    
    if "mystery" in genres:
        story_parts.append(f"Strange clues appeared along the way, and {character_name} had to solve puzzles to continue.")
    
    if "funny" in genres:
        story_parts.append(f"Along the way, {character_name} encountered hilarious situations that made everyone laugh.")
    
    # Resolution
    story_parts.append(f"Through bravery, kindness, and wisdom, {character_name} overcame all obstacles.")
    story_parts.append(f"In the end, {character_name} not only found what they were looking for but also discovered the true treasure was the friends made along the way.")
    story_parts.append("And they all lived happily ever after!")
    
    # Add additional notes if provided
    if notes:
        story_parts.insert(-1, f"As requested: {notes}")
    
    return "\n\n".join(story_parts)





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
            print(email)
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
            print(new_password+" "+cfpassword)
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
