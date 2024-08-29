import speech_recognition as sr

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def convert_audio_to_text(self, audio_file):
        with sr.AudioFile(audio_file) as source:
            audio = self.recognizer.record(source)
            try:
                text = self.recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                print("Unable to recognize speech")
                return None
            except sr.RequestError as e:
                print(f"Error occurred during speech recognition: {e}")
                return None
            
# Example usage in main.py
if __name__ == "__main__":
    stt = SpeechToText()
    text = stt.convert_audio_to_text("audio.wav")
    print(text)