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
		response = ollama.chat(model=self.data['Models'][0], messages=self.data['Prompt'], options={"temperature":0.5})
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
        'ffmpeg','-y', '-stream_loop', '-1', '-i', video_path, '-i', audioPath,
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
	# ("Write a story about a person who discovers a mysterious letter in their attic, leading them on a journey to uncover family secrets long buried.", 3)
	("Create a story where an astronaut, stranded on a distant planet, begins receiving transmissions from a person claiming to be from Earth—but something feels off.", 2)
	("Write about a group of strangers who are brought together by a peculiar event, only to realize their lives have been intertwined in ways they never expected.", 4)
	# ("Imagine a story where an artist finds a paintbrush that brings their paintings to life, but each creation comes with unexpected consequences.", 3)
	("Tell the story of a town where everyone mysteriously forgets the existence of one of its residents, except for one person who fights to prove they were real.", 6)
	("Write about an inventor who creates a time machine, only to find out their future self has been trying to stop them from completing it for a crucial reason.", 2)
	# ("Describe a world where people receive a single, cryptic message at birth, which they must decipher over the course of their lives to understand their purpose.", 3)
	("Tell the story of two enemies forced to team up after discovering they share a long-lost sibling they never knew existed.", 2)
	# ("Write about a seemingly ordinary librarian who uncovers an ancient book that allows them to manipulate reality—but at a steep price.", 5)
	("Create a story about a group of friends who visit a remote village for a reunion, only to discover the village has been stuck in the same day for the past 50 years.",4)
	("Write a story where a long time friend decided to text a friend but has hidden agenda.", 2),
]
video = VideoCreator()
video.create(videos)