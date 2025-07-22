from django.shortcuts import render
import os
from dotenv import load_dotenv
from google import genai
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
def createstory(request):
    if request.method=="POST":
        mc=request.POST.get("characterName")
        age=request.POST.get("age")
        genre=request.POST.getlist("genre")
        story_set=request.POST.get("setting")
        length=request.POST.get("length")
        sp_ele=request.POST.getlist("elements")

        prompt=f"""
                Generate a short children’s story featuring a main character named {mc}, who is {age} years old.
                The story should fall under the following genres: {', '.join(genre)}.
                Set the story in a {story_set} environment, and keep the story approximately {length} long.
                Incorporate the following special elements: {', '.join(sp_ele)}.
                Make it age-appropriate and engaging.
                """
        client = genai.Client()
        response = client.models.generate_content(model="gemini-2.5-flash",contents=prompt,)
  
        return render(request,"stories/createstory.html",{"story":response.text})
    return render(request,"stories/createstory.html")
