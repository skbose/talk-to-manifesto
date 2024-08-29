import requests
import scipy
import os
import numpy as np

class TextToSpeech:
    def __init__(self):
        # TODO: Change URL
        self.url = "https://pjt2thzp99yavt03.us-east-1.aws.endpoints.huggingface.cloud"
        self.headers = {
            "Accept": "application/json",
            "Authorization": "Bearer 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",
            "Content-Type": "application/json"
        }

    def speak(self, text: str, return_speech: bool = False, output_path="") -> dict:
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
                    return {"status": "success", "message": f"Audio saved to {output_path}/speech.wav"}
                else:
                    return {"status": "error", "message": "Unexpected response format"}
            else:
                return speech
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Request failed: {e}"}
        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {e}"}
            

# Example usage in main.py
if __name__ == "__main__":
    tts = TextToSpeech()
    speech = tts.speak("आदरणीय उपस्थित मंडळी, माझ्या भगिनींनो आणि बंधूंनो")
    # Get vector from speech
    vector = speech["audio"][0]
    sampling_rate = speech["sampling_rate"]
