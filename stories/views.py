from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
from dotenv import load_dotenv
from google import genai
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
@login_required
def createstory(request):
    if request.method=="POST":
        mc=request.POST.get("characterName")
        age=request.POST.get("age")
        genre=request.POST.getlist("genre")
        story_set=request.POST.get("setting")
        length=request.POST.get("length")
        sp_ele=request.POST.getlist("elements")

        
        prompt_title = f"""
                Generate a single **short, catchy, and child-friendly title** for a children's story.

                The story features a main character named {mc}, who is {age} years old.
                It should fit the following genres: {', '.join(genre)}.
                The setting is a {story_set} environment.
                The story will be approximately {length} long and include these special elements: {', '.join(sp_ele)}.

                Make sure the title uses **simple words and is easy for children to understand and remember**.
                """
        prompt_story = f"""
                Generate a **short, child-friendly story** for young readers.

                The story should feature a main character named {mc}, who is {age} years old.
                The genres are: {', '.join(genre)}.
                The setting is a {story_set} environment.
                Keep the story approximately {length} long.
                Incorporate the following special elements: {', '.join(sp_ele)}.

                **Important:**
                * Use **simple, straightforward language** and **easy vocabulary**. Avoid complex sentences or jargon.
                * The story should be **age-appropriate and engaging for children**, focusing on clear, positive themes.
                * Ensure the narrative is **easy to follow and understand** for young minds.
                * Focus on dictionary words.
                """
        prompt_moral = """
                Generate a single **simple, clear, and positive moral** for a children's story.

                The moral should be:
                * **Easy for children to understand and remember.**
                * **One or two sentences at most.**
                * Convey a **positive life lesson or value** (e.g., kindness, sharing, bravery, honesty, perseverance).
                * Use **simple, everyday words**.
                """
        client = genai.Client()
        title = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_title)
        story = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_story)
        moral = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_moral)
        elements={}
    
        return render(request,"stories/createstory.html",{"story":story.text,"title":title.text,"moral":moral.text})
    return render(request,"stories/createstory.html")
