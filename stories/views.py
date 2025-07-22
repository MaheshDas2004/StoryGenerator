from django.shortcuts import render
import os
from dotenv import load_dotenv
from google import genai
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
def createstory(request):
    client = genai.Client()

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="give a story on king and queens",)

    print(response.text)
    return render(request,"stories/createstory.html")
