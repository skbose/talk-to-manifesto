import gradio as gr
import scipy.io.wavfile as wavfile
import numpy as np
from scipy.signal import resample
from speech_to_text import SpeechToText

# Initialize the SpeechToText class
speech_to_text = SpeechToText()

def generate_text(audio):
    # audio is a tuple with the first element as sample rate and the second as the audio data
    original_sample_rate, data = audio

    # Target sample rate
    target_sample_rate = 16000

    # Resample the audio data if the original sample rate is different
    if original_sample_rate != target_sample_rate:
        number_of_samples = round(len(data) * target_sample_rate / original_sample_rate)
        data = resample(data, number_of_samples)

    # Ensure data is in int16 format (common format for WAV files)
    data = np.asarray(data, dtype=np.int16)

    # Save the resampled audio
    filename = "output_16000.wav"
    wavfile.write(filename, target_sample_rate, data)
    text = speech_to_text.convert_audio_to_text(filename)
    return f"Audio saved as {filename}. Transcribed text: {text}"

# Create Gradio interface
iface = gr.Interface(
    fn=generate_text, 
    inputs=gr.Audio(type="numpy"), 
    outputs="text",
    title="Record and Save Audio",
    description="Record audio and save it as a WAV file with a sample rate of 16,000 Hz."
)

# Launch the interface
iface.launch()
