from flask import Flask, render_template, request, jsonify, send_from_directory
import speech_recognition as sr
import pyttsx3
import pyjokes
import datetime
import subprocess
import os
import time
from mss import mss  # Using mss instead of pyautogui for screenshots

app = Flask(__name__)

# Initialize the speech engine
engine = pyttsx3.init()
listening = False  # Start with listening disabled

# Folder to save screenshots
SCREENSHOT_FOLDER = "screenshots"
if not os.path.exists(SCREENSHOT_FOLDER):
    os.makedirs(SCREENSHOT_FOLDER)

# 🔹 Define latest_screenshot as a global variable
latest_screenshot = None  

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    """Recognize speech from the microphone."""
    global listening
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        listening = True  
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            return command
        except sr.WaitTimeoutError:
            return "No speech detected."
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand."
        except sr.RequestError:
            return "Speech service unavailable."
        finally:
            listening = False  

def capture_screenshot():
    """Capture a screenshot using the mss library."""
    global latest_screenshot  # 🔹 Declare latest_screenshot as global
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    latest_screenshot = os.path.join(SCREENSHOT_FOLDER, f"screenshot_{timestamp}.png")

    try:
        with mss() as sct:
            sct.shot(output=latest_screenshot)
        return f"Screenshot saved as {latest_screenshot}"
    except Exception as e:
        return f"Failed to capture screenshot: {str(e)}"

def open_application(app_name):
    """Opens applications based on user input."""
    app_paths = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "file explorer": "explorer.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "pycharm": "C:\\Program Files\\JetBrains\\PyCharm Community Edition\\bin\\pycharm64.exe",
        "intellij": "C:\\Program Files\\JetBrains\\IntelliJ IDEA Community Edition\\bin\\idea64.exe",
        "vs code": "C:\\Users\\Ayush\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
    }

    if app_name in app_paths:
        try:
            subprocess.Popen(app_paths[app_name])
            return f"Opening {app_name}..."
        except FileNotFoundError:
            return f"{app_name} not found. Please check the installation path."
    else:
        return f"Application {app_name} not supported."

def open_vscode():
    """Open Visual Studio Code and ask for the programming language."""
    vscode_path = "C:\\Users\\Ayush\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
    try:
        speak("Opening Visual Studio Code")
        subprocess.Popen(vscode_path)
        time.sleep(5)  
        return ask_language()
    except FileNotFoundError:
        return "Visual Studio Code not found. Please check the installation path."

def ask_language():
    """Ask the user for the programming language."""
    speak("Which programming language would you like to use? Python, Java, or C plus plus?")
    command = recognize_speech()
    
    if "python" in command:
        return ask_program_type("python")
    elif "java" in command:
        return ask_program_type("java")
    elif "c++" in command or "c plus plus" in command:
        return ask_program_type("c++")
    else:
        return "I only support Python, Java, and C plus plus."

def ask_program_type(language):
    """Ask what type of program to write."""
    speak(f"What kind of {language} program would you like? Hello World, Fibonacci, or Prime Number?")
    command = recognize_speech()

    if "hello world" in command:
        return write_program(language, "hello world")
    elif "fibonacci" in command:
        return write_program(language, "fibonacci")
    elif "prime number" in command:
        return write_program(language, "prime number")
    else:
        return "I didn't understand the program type."

def write_program(language, program_type):
    """Write the selected program in VS Code."""
    programs = {
        "python": {
            "hello world": ('hello.py', 'print("Hello, World!")'),
            "fibonacci": ('fibonacci.py', 'def fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        print(a, end=" ")\n        a, b = b, a + b\nfib(10)'),
            "prime number": ('prime.py', 'def is_prime(n):\n    if n < 2: return False\n    for i in range(2, int(n ** 0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\nprint(is_prime(19))')
        }
    }

    if language in programs and program_type in programs[language]:
        filename, code = programs[language][program_type]
        filepath = os.path.join(os.getcwd(), filename)

        with open(filepath, "w") as file:
            file.write(code)

        speak(f"Writing a {program_type} program in {language}")
        subprocess.Popen(["code", filepath])
        return f"Writing a {program_type} program in {language}..."
    else:
        return "I couldn't write the requested program."

def open_latest_screenshot():
    """Opens the latest screenshot in the default image viewer."""
    global latest_screenshot  # 🔹 Ensure we are using the global variable

    if latest_screenshot and os.path.exists(latest_screenshot):
        subprocess.run(["start", latest_screenshot], shell=True)
        return "Opening the latest screenshot..."
    return "No screenshot available. Capture a screenshot first."

def joke():
    pyjokes.get_jokes()

import wikipedia

def execute_command(command):
    """Execute commands based on recognized speech."""
    global latest_screenshot  

    command = command.lower()

    if 'write hello world in python' in command:
        return write_program('python', 'hello world')
    elif 'write hello world in java' in command:
        return write_program('java', 'hello world')
    elif 'write fibonacci program in python' in command:
        return write_program('python', 'fibonacci')
    elif 'write prime number program in java' in command:
        return write_program('java', 'prime number')
    elif 'write hello world in c++' in command or 'write hello world in c plus plus' in command:
        return write_program('c++', 'hello world')
    
    elif 'open python ide' in command:
        return open_application('pycharm')  # Open PyCharm for Python
    elif 'open java ide' in command:
        return open_application('intellij')  # Open IntelliJ IDEA for Java
    elif 'open c++ ide' in command or 'open c plus plus ide' in command:
        return open_application('vs code')  # Open VS Code for C++

    elif 'open visual studio code' in command:
        return open_vscode()

    elif 'capture screenshot' in command or 'take screenshot' in command:
        return capture_screenshot()
    
    elif 'show screenshot' in command:
        return open_latest_screenshot()
    
    elif 'tell me a joke' in command or 'say a joke' in command:
        joke = pyjokes.get_joke()
        speak(joke)
        return joke
    
    elif 'exit' in command or 'goodbye' in command:
        speak("Goodbye!")
        return "Goodbye!"
    
    elif 'open' in command:
        app_name = command.replace('open ', '').strip()
        return open_application(app_name)
    
    return "I didn't understand that command."

@app.route('/speak', methods=['POST'])
def on_speak():
    """Process speech input and execute commands."""
    global listening
    if listening:
        return jsonify({"status": "error", "response": "Already listening..."})
    
    result = recognize_speech()
    response = execute_command(result) if result else "No command recognized."

    return jsonify({
        "status": "success",
        "user_command": result,
        "response": response
    })

@app.route('/screenshots/<filename>')
def serve_screenshot(filename):
    """Serve the screenshot file."""
    return send_from_directory(SCREENSHOT_FOLDER, filename)

@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
