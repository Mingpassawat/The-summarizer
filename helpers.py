import openai
from pytube import YouTube

from flask import redirect, render_template, request, session
from functools import wraps

API = ""

# Load API
openai.api_key = API

def yt_to_mp3(link, name, id):
    yt = YouTube(link)

    dowloader = yt.streams.filter(only_audio=True).get_audio_only()

    dowloader.download(filename=f"{name}.mp3", output_path=f"static/files/{id}/")

    # Return title
    return yt.title

def transcription(filepath):    
    audio_file = open(filepath, 'rb')
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

def summarize(transcript):
    content = f"""
        {transcript}

    Summarize this youtube video trascript and do a paragraph break too
    """

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             'content': content}
        ]
    )
    return completion.choices[0].message['content']

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def embed(url):
    if url[:24] == "https://www.youtube.com/":
        v = url[32:]
        return "https://www.youtube.com/embed/" + v

    elif url[:17] == "https://youtu.be/":
        v = url[17:]
        return "https://www.youtube.com/embed/" + v
    else: 
        return url



if __name__ == "__main__":

    link = input()

    yt_to_mp3(link, "audio", 0)

    filepath = "audio.mp3"
    transcript = transcription(filepath)
    print(transcript)

    print(summarize(transcript))

