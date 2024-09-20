import logging
import os

import numpy as np
import requests
import scipy

from ai_hub.modules.tts.base_tts import BaseTTS
from ai_hub.modules.tts.utils import split_into_lines

logger = logging.getLogger(__name__)
logging.basicConfig(filename="tts.log", encoding="utf-8", level=logging.DEBUG)


class HuggingFaceTTS(BaseTTS):
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
            "Content-Type": "application/json",
        }

    def _convert_to_int16(self, audio: np.ndarray):
        """
        Convert audio to int16
        """
        return np.int16(audio / np.max(np.abs(audio)) * np.iinfo(np.int16).max)

    def synthesize(self, text: str):
        """
        Request through HuggingFace TTS API
        """
        data = self._prepare_inputs(text)
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
            response.raise_for_status()
            response_dict = response.json()
            if "audio" in response_dict and "sampling_rate" in response_dict:
                # convert audio to int16
                audio_int16 = self._convert_to_int16(response_dict.get("audio"))
                return {
                    "audio": audio_int16,
                    "sampling_rate": response_dict.get("sampling_rate"),
                }
            else:
                logger.error(f"No audio/sampling_rate in response: {response_dict}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

    def _prepare_inputs(self, text: str):
        """
        Prepare inputs for HuggingFace TTS API
        """
        return {"inputs": text, "parameters": {}}

    def stream(self, text: str):
        """
        Stream audio for the given text
        """
        lines = split_into_lines(text)
        for line in lines:
            speech = self.synthesize(line)
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
                data=np.array(speech["audio"][0]),
            )
            logger.debug(f"Saved audio to {os.path.join(output_dir, f'{i}.wav')}")


if __name__ == "__main__":
    # read token from .env file
    from dotenv import load_dotenv

    load_dotenv(override=True)

    tts = HuggingFaceTTS(url=os.getenv("HF_TTS_URL"), token=os.getenv("HF_TOKEN"))
    tts.stream_and_save(
        text="आदरणीय उपस्थित मंडळी, माझ्या भगिनींनो आणि बंधूंनो", output_dir="output"
    )
