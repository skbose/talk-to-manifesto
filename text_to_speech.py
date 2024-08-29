import pyttsx3

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()

    def convert(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

# Example usage in main.py
if __name__ == "__main__":
    tts = TextToSpeech()
    tts.speak("Hello, world!")