from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import wave
import re
from stories.models import Story

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
def sanitize_story_text(text):
    return re.sub(r'[^A-Za-z0-9 .,!?\'\n]+', '', text)
@login_required

def createstory(request):
    if request.method == "POST":
        message = request.POST.get("message")
        genre = request.POST.get("genre")
        setting = request.POST.get("setting")
        time_period = request.POST.get("timePeriod")
        main_character = request.POST.get("mainCharacter")
        character_age = request.POST.get("characterAge")
        character_description = request.POST.get("characterDescription")
        special_request = request.POST.get("specialRequest")
        tone = request.POST.get("tone")
        length = request.POST.get("length")
        themes = request.POST.get("themes")
        theme_list = themes.split(",")
        
        story_prompt = f"""
            Write a {length or 'short'} {genre.lower()} story with a {tone.lower() if tone else 'light'} tone.
            The story should be set in {setting or 'an imaginative place'} during {time_period or 'modern times'}.
            The main character is {main_character} ({character_age or 'young'}), {character_description or 'a curious and brave soul'}.
            The story should deliver a message: "{message}".
            Themes to include: {', '.join(theme_list) if themes else 'any inspiring theme'}.
            {"Include: " + special_request if special_request else ""}
            Keep the language simple and suitable for children.
            """
        client = genai.Client()
        story = client.models.generate_content(model="gemini-2.5-flash", contents=story_prompt)
        story_txt=sanitize_story_text(story.text)

        title_prompt = f"""
            Read the story below and generate a short, unique, and creative title.
            Avoid using punctuation or quotation marks. Return only the title text.

            Story:
            {story_txt}
            """
        title = client.models.generate_content(model="gemini-2.5-flash", contents=title_prompt)
        title_txt=sanitize_story_text(title.text)

        moral_prompt = f"""
            Read the story below and generate a short and meaningful moral or takeaway.
            Make it sound natural and relevant to the story’s events.
            Return only the moral sentence.

            Story:
            {story_txt}
            """
        moral = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=moral_prompt
        )
        moral_txt = sanitize_story_text(moral.text)
        request.session['title']=title_txt
        request.session['story']=story_txt
        request.session['moral']=moral_txt
        request.session['genre']=genre
        request.session['setting']=setting

        return redirect("view_story")
    return render(request,"stories/createstory.html")

# def view_story(request, story_id):

#     story = Story.objects.get(id=story_id, user=request.user)
#     return render(request, "stories/storyview.html", {
#         "title": story.title,
#         "story": story.content,
#         "moral": story.moral
#     })
def viewstory(request,story_id=None):
    if(story_id):
        story = Story.objects.get(id=story_id, user=request.user)
        return render(request, "stories/storyview.html", {
        "title": story.title,
        "story": story.content,
        "moral": story.moral,
        "saved":True
    })

    title = request.session.get("title")
    story = request.session.get("story")
    moral = request.session.get("moral")
    return render(request, "stories/storyview.html", {
        "title": title,
        "story": story,
        "moral": moral,
        "saved":False
    })


def savestory(request):
    if request.method == "POST":
        title = request.session.get("title")
        story = request.session.get("story")
        moral = request.session.get("moral")
        genre = request.session.get("genre")
        setting = request.session.get("setting")

        story_obj=Story.objects.create(user=request.user,title=title,moral=moral,content=story,genre=genre,setting=setting)
        for key in ['title', 'story', 'moral', 'genre', 'setting']:
            request.session.pop(key, None)

        return redirect("view_saved_story",story_id=story_obj.id)

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