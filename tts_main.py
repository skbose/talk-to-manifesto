import gradio as gr
from text_to_speech import TextToSpeech

text_to_speech = TextToSpeech()

# Define the Gradio interface
def generate_output(text):
    # Convert search result to speech
    speech = text_to_speech.speech(text, return_speech = True)
    return speech

# Create the Gradio interface
gr.Interface(fn=generate_output, inputs="text", outputs="audio").launch()
