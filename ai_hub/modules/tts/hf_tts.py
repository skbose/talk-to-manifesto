import requests
import scipy
import os
import numpy as np
from ai_hub.modules.tts.base import TTSBase
from ai_hub.modules.tts.utils import split_into_lines

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='tts.log', encoding='utf-8', level=logging.DEBUG)


class HuggingFaceTTS(TTSBase):
    def __init__(self, url: str, token: str):
        """
        Args:
            url (str): HuggingFace TTS API URL
        """
        self.url = url
        self.token = token
        self.headers = self._prepare_header()

        logger.debug(f"Request Headers: {self.headers}")

    def _prepare_header(self):
        """
        Prepare header for HuggingFace TTS API
        """
        assert self.token is not None, "HF Token is not set"
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def synthesize(self, data: dict):
        """
        Request through HuggingFace TTS API
        """
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

    def stream(self, text: str):
        """
        Stream audio for the given text
        """
        lines = split_into_lines(text)
        for line in lines:
            data = {
                "inputs": line,
                "parameters": {}
            }
            speech = self.synthesize(data)
            if speech:
                yield speech

    def stream_and_save(self, text: str, output_dir: str) -> None:
        """
        Synthetize and save audio for the given text (should be)
        """
        # create output dir if not exists
        os.makedirs(output_dir, exist_ok=True)

        for i, speech in enumerate(self.stream(text)):
            scipy.io.wavfile.write(
                os.path.join(output_dir, f"{i}.wav"),
                rate=speech["sampling_rate"],
                data=np.array(speech["audio"][0])
            )
            logger.debug(f"Saved audio to {os.path.join(output_dir, f'{i}.wav')}")


if __name__ == "__main__":
    # read token from .env file
    from dotenv import load_dotenv
    load_dotenv(override=True)

    tts = HuggingFaceTTS(
        url="https://a70oxw6lqxzz0jxp.us-east-1.aws.endpoints.huggingface.cloud",
        token=os.getenv("HF_TOKEN")
    )
    tts.stream_and_save(text="आदरणीय उपस्थित मंडळी, माझ्या भगिनींनो आणि बंधूंनो", output_dir="output")
