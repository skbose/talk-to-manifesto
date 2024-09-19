import base64
import logging
import os

import requests

from ai_hub.modules.stt.base_stt import BaseSTT

logger = logging.getLogger(__name__)
logging.basicConfig(filename="stt.log", encoding="utf-8", level=logging.DEBUG)


class HuggingFaceSTT(BaseSTT):
    def __init__(self, url: str, token: str):
        """
        Args:
            url (str): HuggingFace STT API URL
        """
        self.url = url
        self.token = token
        self.headers = self._prepare_header()

    def _prepare_header(self):
        """
        Prepare header for HuggingFace STT API
        """
        assert self.token is not None, "HF Token is not set"
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _prepare_payload(self, audio_file: str) -> dict:
        """
        Prepare payload for HuggingFace STT API
        """
        assert os.path.exists(audio_file), "Audio file does not exist"
        logger.debug(f"Loading audio file: {audio_file}")

        with open(audio_file, "rb") as f:
            audio_bytes = f.read()

        # base64 encode the audio file (url safe)
        audio_bytes = base64.urlsafe_b64encode(audio_bytes).decode("utf-8")

        audio_data = {
            "inputs": audio_bytes,
        }

        return audio_data

    def extract_text(self, audio_file: str) -> str:
        """
        Extract text from audio file
        """
        assert os.path.exists(audio_file), "Audio file does not exist"

        audio_data = self._prepare_payload(audio_file)
        response = requests.post(
            self.url, headers=self.headers, json=audio_data
        )

        if response.status_code != 200:
            raise Exception(
                f"Failed to extract text from audio file. Status code: \
                {response.status_code}, Response: {response.text}"
            )

        return response.json()["text"]


if __name__ == "__main__":
    # read token from .env file
    from dotenv import load_dotenv

    load_dotenv(override=True)

    stt = HuggingFaceSTT(
        url=os.getenv("HF_STT_URL"), token=os.getenv("HF_TOKEN")
    )
    print(stt.extract_text("output/0.wav"))
