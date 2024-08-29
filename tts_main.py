import gradio as gr
from text_to_speech import TextToSpeech

text_to_speech = TextToSpeech()

# Define the Gradio interface
def generate_output(text):
    # Convert search result to speech
    return_speech_wav = True
    if return_speech_wav:
        speech_path = text_to_speech.convert(text, return_speech = return_speech_wav)
        return open(speech_path, "rb")
    else:
        speech = text_to_speech.convert(text, return_speech = return_speech_wav)
        return speech

# Create the Gradio interface
gr.Interface(fn=generate_output, inputs="text", outputs="audio").launch()
