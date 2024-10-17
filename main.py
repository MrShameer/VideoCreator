from pyht import Client
from pydub import AudioSegment
from pyht.client import TTSOptions
import os, ollama, json, random, subprocess, shutil

class VideoCreator():
	def __init__(self) -> None:
		if os.path.exists("Process"):
			shutil.rmtree("Process")
		os.makedirs(f"FinalVideos", exist_ok=True)
		self.voiceClient = Client(
			user_id=os.getenv("PLAY_HT_USER_ID"),
			api_key=os.getenv("PLAY_HT_API_KEY"),
			auto_connect=False
		)
		self.audioPath = ""
		self.videoFiles = [f for f in os.listdir("RandomVideos") if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]

		with open('config.json', 'r') as file:
			self.data = json.load(file)
		self.data['Prompt'][0]['content'] = self.data['Prompt'][0]['content'].replace('CHARACTER_LIST', str(list(self.data['Characters'].keys())))

	def generateStory(self, story, max):
		self.data['Prompt'][1]['content'] = story
		self.data['Prompt'][0]['content'] = self.data['Prompt'][0]['content'].replace('CHARACTER_LIMIT', str(max))
		response = ollama.chat(model=self.data['Models'][0], messages=self.data['Prompt'])
		self.script = json.loads(response['message']['content'].replace('```json', '').replace('```', ''))
		print(self.script)
		return self.script

	def createAudios(self, num, script):
		os.makedirs(f"Process/{num}/Audios/", exist_ok=True)
		combinedAudio = AudioSegment.empty()
		for index, dialog in enumerate(script):
			options = TTSOptions(voice=self.data['Characters'][dialog["Character"]])
			audioPath = f"Process/{num}/Audios/{index}-{dialog["Character"]}.mp3"
			with open(audioPath, "ab") as f:
				for chunk in self.voiceClient.tts(dialog["Dialog"], options):
					f.write(chunk)

			audio_segment = AudioSegment.from_file(audioPath)
			combinedAudio += audio_segment
		return combinedAudio.export(f"Process/{num}/finalAudio.mp3", format="mp3")
	
	def createVideos(self, num, audioPath):
		video_path = f"RandomVideos/{random.choice(self.videoFiles)}"

		command = [
        'ffmpeg','-y','-i', video_path, '-i', audioPath,
        '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0',
        '-shortest', f'FinalVideos/{num}-Video.mp4'
    	]

		subprocess.run(command, check=True)
		print("Output", f'FinalVideos/{num}-Video.mp4')

	def create(self, stories):
		for index, story in enumerate(stories):
			print(story)
			audio = self.createAudios(index, self.generateStory(*story))
			self.createVideos(index, audio.name)

videos = [
	("Write a story where a long time friend decided to text a friend but has hidden agenda, and make it really engaging make the store in like a text message perspective. Make the story interesting, with triller, and keeps readers hooked up and on their toes. Add suspense if needed.", 2),
	# ("write a happy story", 5)
]
video = VideoCreator()
video.create(videos)