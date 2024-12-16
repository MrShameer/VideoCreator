# AI Brainrot TikTok Video Generator

This script generates "**Brainrot**" TikTok videos by combining a random background, an AI-generated story (using [Ollama's Gemma2](https://ollama.com/library/gemma2) LLM), and Text to speech voices (via [play.ht's Text-to-Speech API](https://play.ht/text-to-speech-api/python/)). The final output is a complete video ready for upload.

## Features
- **Story Generation**: Uses the Gemma2 LLM to generate creative and quirky stories.
- **Text-to-Speech**: Converts the story into character voices using play.ht's API.
- **Random Backgrounds**: Automatically selects a random video or image as the background.
- **Configurable Characters**: Modify character names and system prompts in a JSON file.
- **Simple Execution**: Run the script with a single command.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MrShameer/VideoCreator.git
   cd VideoCrator
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Edit the `config.json` file to modify:
- **Characters**: Names of the characters used in the generated story.
- **LLM System Prompt**: Customize the storytelling style or theme.
- **Model**: Change LLM model.
- **Videos**: Put videos that can be used for the background into the `RandomVideos/` folder.

---

## Voice Selection

You can get a **list of available voices** from play.ht's documentation [here](https://docs.play.ht/reference/python-sdk). Update the `"id"` field for each character in the `config.json` file to match one of the supported voice IDs.

---

## How to Run

1. Ensure the `config.json` file is configured to your liking.
2. Put videos that can be used for the background into the `RandomVideos/` folder.
3. Run the script:
   ```bash
   python main.py
   ```

The script will:
1. Generate a story using Gemma2 or any LLM models according to your preferences.
2. Use play.ht to generate audio for each character in the story.
3. Combine the audio with a random background video or image.
4. Output the final video to the `Output/` directory.

---

## Requirements

The `requirements.txt` file includes all dependencies:
```
ollama
pydub
pyht
```

Make sure you have API keys set up for:
- **play.ht** (Text-to-Speech API)

---

## Contribution

Feel free to fork and modify this script to add more features or improve its functionality. Pull requests are welcome!

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Notes
- Make sure you have sufficient credits in play.ht for TTS generation.
- The RandomVidos folder should contain videos.

Happy brainrotting! 😵‍💫
