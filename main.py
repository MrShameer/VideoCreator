from pyht import Client
from pydub import AudioSegment
from pyht.client import TTSOptions
import os
import io
import ollama
import json

client = Client(
    user_id=os.getenv("PLAY_HT_USER_ID"),
    api_key=os.getenv("PLAY_HT_API_KEY"),
)

audio={
    "Sarah":"s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json",
    "John":"s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json",
}


response = ollama.chat(model='gemma2', messages=[
  {
    'role': 'system',
    'content': """You are an AI tasked to generate an interesting story based on the prompt from the user and make sure the story is in a form of dialogs only. 
    Use only 2 characters 'Sarah' and 'John'. The output should be in a json format where it should have a list containing a key called 'Character' with their name as the value and a key called 'Dialog' with their dialog as their value. 
    Respond with only a JSON output according to the format and no preamble and no any explanation""",

  }, 
  {
    'role': 'user',
    'content':'write a horror story'
  }
]
# stream=True,
)
# for chunk in response:
#   print(chunk['message']['content'], end='', flush=True)
print(response['message']['content'])
script=json.loads(response['message']['content'].replace('```json', '').replace('```', '')) 
print(script)


for index, dialog in enumerate(script):
    print(dialog["Character"],dialog["Dialog"])
    options = TTSOptions(voice=audio[dialog["Character"]])
    with open(f"Audios/{dialog["Character"]} {index}.mp3", "wb") as f:
        for chunk in client.tts(dialog["Dialog"], options):
            f.write(chunk)