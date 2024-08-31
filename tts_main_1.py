import gradio as gr
from text_to_speech import TextToSpeech
import numpy as np

text_to_speech = TextToSpeech()

# Define the Gradio interface
def generate_output(text):
    # Convert search result to speech
    audio = np.array([])
    for speech in  text_to_speech.convert_stream(text):
        audio = np.concatenate([audio, np.array(speech["audio"][0])])
        yield speech['sampling_rate'], audio

# Create the Gradio interface
gr.Interface(fn=generate_output, inputs="text", outputs=gr.Audio(autoplay=True)).queue().launch()
