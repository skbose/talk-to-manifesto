import gradio as gr
from text_to_speech import TextToSpeech
import numpy as np

text_to_speech = TextToSpeech()

# Define the Gradio interface
def generate_output(text):
    # Convert search result to speech
    speech = text_to_speech.convert(text, return_speech = False)
    return speech["sampling_rate"], np.array(speech["audio"][0])

# Create the Gradio interface
gr.Interface(fn=generate_output, inputs="text", outputs="audio").launch()
