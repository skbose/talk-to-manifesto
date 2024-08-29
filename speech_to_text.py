import torch
from transformers import pipeline
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import librosa
import soundfile as sf
import os

class SpeechToText:
    def __init__(self):
        # Setup Model
        processor = AutoProcessor.from_pretrained("DrishtiSharma/whisper-large-v2-marathi")
        model = AutoModelForSpeechSeq2Seq.from_pretrained("DrishtiSharma/whisper-large-v2-marathi")
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        # Send model to device
        model.to(device)

        # Setup speech to text inference pipeline
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device,
            generate_kwargs={"suppress_tokens": None}
        )

    def convert_audio_to_text(self, audio_file):
        temp_file = None
        try:
            # Check if audio file is a .wav file
            if not audio_file.endswith('.wav'):
                # Load and resample the audio to 16kHz, which is commonly used in ASR models
                y, sr = librosa.load(audio_file, sr=16000)
                # Save the resampled audio to a temporary file
                temp_file = "temp_audio.wav"
                sf.write(temp_file, y, sr)
                audio_file = temp_file

            # Perform speech-to-text conversion
            result = self.pipe(audio_file)
            output = result["text"].lstrip()
            return output

        except FileNotFoundError:
            print(f"Error: The file {audio_file} was not found.")
            return None

        except ValueError as ve:
            print(f"Value Error: {ve}")
            return None

        except Exception as e:
            print(f"An error occurred during audio processing: {e}")
            return None

        finally:
            # Clean up the temporary file if it was created
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)
            
# Example usage in main.py
if __name__ == "__main__":
    stt = SpeechToText()
    text = stt.convert_audio_to_text("audio.wav")
    print(text)
