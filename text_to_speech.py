import requests
import scipy
import os
import numpy as np
import re
import time


def split_into_lines(text):
    # This pattern splits the text at '.', '?', '!', but keeps the delimiter
    lines = re.split(r'(?<=[.?!])\s+', text.strip())
    return lines

class TextToSpeech:
    def __init__(self):
        HF_TOKEN = "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"
        # TODO: CPU API
        self.url = "https://a70oxw6lqxzz0jxp.us-east-1.aws.endpoints.huggingface.cloud"
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        }

    def convert(self, text: str, return_speech: bool = False, output_path=""):
        data = {
            "inputs": text,
            "parameters": {}
        }
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
            response.raise_for_status()
            speech = response.json()
            if return_speech:
                # Assuming the API returns 'sampling_rate' and 'audio' keys in the response
                if "sampling_rate" in speech and "audio" in speech:
                    scipy.io.wavfile.write(
                        os.path.join(output_path, "speech.wav"),
                        rate=speech["sampling_rate"],
                        data=np.array(speech["audio"][0])
                    )
                    return os.path.join(output_path, "speech.wav")
                else:
                    return {"status": "error", "message": "Unexpected response format"}
            else:
                return speech
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Request failed: {e}"}
        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {e}"}

    def convert_stream(self, text: str):
        sentences = split_into_lines(text)
        sentences = [sentence.strip() for sentence in sentences if sentence]
        
        for sentence in sentences:
            data = {
                "inputs": sentence,
                "parameters": {}
            }
            response = requests.post(self.url, headers=self.headers, json=data)
            response.raise_for_status()
            speech = response.json()
            yield speech

# Example usage in main.py
if __name__ == "__main__":
    tts = TextToSpeech()
    speech = tts.convert("आदरणीय उपस्थित मंडळी, माझ्या भगिनींनो आणि बंधूंनो")

    # Get vector from speech
    vector = speech["audio"][0]
    sampling_rate = speech["sampling_rate"]

    # Save the audio file
    output_file = "output_speech.wav"
    scipy.io.wavfile.write(output_file, rate=sampling_rate, data=np.array(vector))
    print(f"Speech saved to {output_file}")
