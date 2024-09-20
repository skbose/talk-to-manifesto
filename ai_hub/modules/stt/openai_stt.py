# OpenAI STT class

from openai import OpenAI
import os
from dotenv import load_dotenv


class OpenAIStt:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def extract_text(self, audio_file: str) -> str:
        with open(audio_file, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            return transcription.text


if __name__ == "__main__":
    load_dotenv(override=True)
    openai_stt = OpenAIStt(api_key=os.getenv("OPENAI_API_KEY"))
    print(openai_stt.extract_text("output/0.wav"))
