from pyht import Client
from pydub import AudioSegment
from pyht.client import TTSOptions
import os, ollama, json, random, subprocess, shutil, uuid

class VideoCreator():
	def __init__(self) -> None:
		if os.path.exists("Process"):
			shutil.rmtree("Process")
		os.makedirs(f"FinalVideos", exist_ok=True)
		os.makedirs(f"FinalScripts", exist_ok=True)
		self.voiceClient = Client(
			user_id=os.getenv("PLAY_HT_USER_ID"),
			api_key=os.getenv("PLAY_HT_API_KEY"),
			auto_connect=False
		)
		self.audioPath = ""
		self.uid = None
		self.videoFiles = [f for f in os.listdir("RandomVideos") if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
		
		with open('config.json', 'r') as file:
			self.data = json.load(file)
		
		character_list = list(self.data['Characters'].keys())
		self.data['Prompt'][0]['content'] = self.data['Prompt'][0]['content'].replace('{CHARACTER_LIST}', str(character_list))
	
	def generateStory(self, story, max_characters):
		self.data['Prompt'][1]['content'] = story
		self.data['Prompt'][0]['content'] = self.data['Prompt'][0]['content'].replace('{CHARACTER_LIMIT}', str(max_characters))
		response = ollama.chat(model=self.data['Models'][0], messages=self.data['Prompt'], format='json', options={"temperature":0.5, "num_ctx":16384})
		return json.loads(response['message']['content'].replace('```json', '').replace('```', ''))
	
	def createAudios(self, script):
		os.makedirs(f"Process/{self.uid}/Audios/", exist_ok=True)
		combinedAudio = AudioSegment.empty()
		for index, dialog in enumerate(script):
			print(dialog)
			options = TTSOptions(voice=self.data['Characters'][dialog["Character"]]["id"])
			audioPath = f"Process/{self.uid}/Audios/{index}-{dialog['Character']}.mp3"
			with open(audioPath, "ab") as f:
				for chunk in self.voiceClient.tts(dialog["Dialog"], options):
					f.write(chunk)
			
			audio_segment = AudioSegment.from_file(audioPath)
			combinedAudio += audio_segment
		
		return combinedAudio.export(f"Process/{self.uid}/finalAudio.mp3", format="mp3")
	
	def createVideos(self, audioPath):
		video_path = f"RandomVideos/{random.choice(self.videoFiles)}"
		
		command = [
			'ffmpeg', '-y', '-stream_loop', '-1', '-i', video_path, '-i', audioPath,
			'-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0',
			'-shortest', f'FinalVideos/{self.uid}-Video.mp4'
		]
		
		subprocess.run(command, check=True)
		print(f"Output: FinalVideos/{self.uid}-Video.mp4")
	
	def create(self, stories):
		for index, story in enumerate(stories):
			print(f"Processing story {index+1}: {story}")
			script = self.generateStory(*story)
			print("Generated Script:", script)
			self.uid = f"{index}-{str(uuid.uuid4())}"
			with open(f"FinalScripts/{self.uid}.json", "w") as outfile:
				json.dump(script, outfile)
			audio = self.createAudios(script)
			self.createVideos(audio.name)


videos = [
	(
		"""Write a story for a TikTok video set in a busy urban environment. The story follows two characters who are best friends working at the same company. 
		They are both up for a big promotion, but there is a secret: one of the character has discovered that other person might be sabotaging their chances. 
		The story unfolds in a series of tense confrontations, starting with friendly banter and escalating into suspicion, betrayal, 
		and an unexpected twist that changes everything. Use sharp, punchy dialogue to build suspense, with each character hiding something from the other. 
		The twist should be both shocking and emotionally engaging, leaving the audience wanting more.""", 2),
	 
	# ("""Write a story for a TikTok video featuring Amir, Ana, and Sam. Amir and Sam are secretly crushing on each other but are too shy to admit it. 
	#  Ana, their mutual friend and notorious for trolling, notices the chemistry between them and decides to have some fun. 
	#  The story starts with Amir and Sam awkwardly trying to spend time together, but Ana continuously interrupts, 
	#  making sarcastic comments and setting up humorous dialogue to make them flustered. As the tension builds, Ana's trolling gets out of hand, 
	#  and Amir and Sama give up on confront each other about their feelings in an dissapointed way. Add humor, drama, 
	#  and an unexpected twist at the end that resolves the tension in a surprising and heartwarming way. 
	#  Keep the dialogue brief and punchy for a TikTok video lasting about 1 minute.""", 3)
]

video = VideoCreator()
video.create(videos)
