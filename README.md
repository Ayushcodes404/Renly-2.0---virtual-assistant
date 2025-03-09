# Voice Assistant using Flask

A smart voice assistant built using Flask, Speech Recognition, and Python automation libraries. This assistant can recognize voice commands, open applications, write code, capture screenshots, and more.

## Features 🚀

- 🎤 **Speech Recognition**: Understands voice commands using `speech_recognition`
- 🔊 **Text-to-Speech**: Responds with voice output using `pyttsx3`
- 🖥️ **Application Launcher**: Opens commonly used applications like VS Code, Chrome, Notepad, etc.
- 📸 **Screenshot Capture**: Takes and displays screenshots using `mss`
- 🤖 **Automated Code Writing**: Writes Python, Java, and C++ programs based on voice commands
- 😆 **Joke Generator**: Tells programming jokes with `pyjokes`
- 📚 **Wikipedia Search**: Retrieves information from Wikipedia

## Installation 🛠️

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/voice-assistant.git
   cd voice-assistant
   ```
2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage 📌

1. **Run the Flask app:**
   ```bash
   python app.py
   ```
2. **Interact with the assistant:**
   - Say "Open Visual Studio Code" to launch VS Code.
   - Say "Capture screenshot" to take a screenshot.
   - Say "Write Fibonacci program in Python" to generate code.
   - Say "Tell me a joke" for a fun response.

## Dependencies 📦

Make sure you have the following Python packages installed:

- Flask
- SpeechRecognition
- pyttsx3
- pyjokes
- datetime
- subprocess
- mss
  
Install all dependencies using:
```bash
pip install -r requirements.txt
```

## Contribution 🤝

Feel free to fork, modify, and contribute to this project. Create a pull request if you have improvements or new features!

---
Made with ❤️ by Ayush (https://github.com/ayushcodes404)


