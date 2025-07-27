from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import wave
import re


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
def sanitize_story_text(text):
    return re.sub(r'[^A-Za-z0-9 .,!?\'\n]+', '', text)
@login_required


def createstory(request):

    if request.method=="POST":
        if request.POST.get("step1"):
            genre=request.POST.get("genre")
            character=request.POST.get("character")
            story_set=request.POST.get("setting")
            params={
                'genre':genre,
                "character":character,
                "setting":story_set,
            }
            params["setstep2"]=True
            return render(request,"stories/createstory.html",params)
        
        if request.POST.get("step2"):
            genre=request.POST.get("genre")
            character=request.POST.get("character")
            story_set=request.POST.get("setting")
            child_name=request.POST.get("child_name")
            child_age=request.POST.get("child_age")
            story_length=request.POST.get("story_length")
            story_lesson=request.POST.get("story_lesson")
            special_request=request.POST.get("special_request")
            
            prompt_story=f"""You are a creative AI that writes fun and easy-to-understand stories for kids.

                            Please write a short story using the information below:

                            - Genre: { genre }
                            - Main Character Type: { character }
                            - Story Setting: { story_set }
                            - Child’s Name: { child_name }
                            - Child’s Age: { child_age }
                            - Story Length: Around { story_length } words
                            - Special Request: { special_request }
                            - Theme for inspiration: { story_lesson }

                            Instructions:
                            - Make { child_name } the main character of the story.
                            - Use very simple and friendly words so that a { child_age }-year-old child can understand easily.
                            - Set the story in { story_set } and include a character like {character}.
                            - The story should feel inspired by "{ story_lesson }", but do **not** include a “moral of the story” or write any separate moral line.
                            - **Avoid all special characters** like ! @ # $ % ^ & * etc.
                            - Do not write a title or heading — only the story.
                            - Avoid hard English, sad topics, or anything scary.

                            Write like you are telling a happy and magical story to a child."""
            client = genai.Client()
            story = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_story)
            story_txt=sanitize_story_text(story.text)
                                    
            prompt_title = f"""
                            You are a children's storyteller and educator.
                            I will give you a short story meant for a child (age: {child_age}). 
                            Based on that story, do the following:

                            1. Generate a creative and fun title using very simple and child-friendly words. Do not use any special characters or punctuation marks in the title.
                            Make sure:
                            - No complicated vocabulary is used.
                            - The title must be short and not contain symbols like !, @, #, etc.
                            - output must be plain text and friendly for kids.

                            Story:
                            {story_txt}
                            """
            title = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_title)
            title_txt=sanitize_story_text(title.text)

            prompt_moral = f"""
                            You are a children's storyteller and educator.
                            I will give you a short story meant for a child (age: {child_age}). 
                            Based on that story, do the following:

                            1. Write a simple and meaningful moral that a child can easily understand. The moral should teach or inspire something positive based on the story.

                            Make sure:
                            - No complicated vocabulary is used.
                            - The title must be short and not contain symbols like !, @, #, etc.
                            - output must be plain text and friendly for kids.

                            Story:
                            {story_txt}
                            """
            moral = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_moral)

            moral_txt=sanitize_story_text(moral.text)


            return render(request,"stories/createstory.html",{"story":story_txt,"title":title_txt,"moral":moral_txt})
    
    if request.GET.get("saveStory"):
        params={}
    return render(request,"stories/createstory.html",{"setstep1":True})

# def generateAudio(request):
#     client = genai.Client()
#     response = client.models.generate_content(
#     model="gemini-2.5-flash-preview-tts",
#     contents=f"say as if you are narrating story to children with full of emotions and expressions :\n\n{xyz}",
#     config=types.GenerateContentConfig(
#         response_modalities=["AUDIO"],
#         speech_config=types.SpeechConfig(
#             voice_config=types.VoiceConfig(
#                 prebuilt_voice_config=types.PrebuiltVoiceConfig(
#                 voice_name='Sulafat',
#                 )
#             )
#         ),
#     )
#     )
#     data = response.candidates[0].content.parts[0].inline_data.data

#     file_name='out.wav'
# def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
#    with wave.open(filename, "wb") as wf:
#       wf.setnchannels(channels)
#       wf.setsampwidth(sample_width)
#       wf.setframerate(rate)
#       wf.writeframes(pcm)
#     wave_file(file_name, data) # Saves the file to current directory