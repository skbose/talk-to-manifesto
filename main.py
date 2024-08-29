import gradio as gr
from speech_to_text import SpeechToText
from text_to_text_search import TextToTextSearch
from text_to_speech import TextToSpeech

# Initialize the three main classes
speech_to_text = SpeechToText()
text_to_text_search = TextToTextSearch()
text_to_speech = TextToSpeech()

# Define the Gradio interface
def generate_output(sound):
    # Convert sound to text
    text = speech_to_text.convert_audio_to_text(sound)

    # Search for relevant text
    search_result = text_to_text_search.search(text)

    # Convert search result to speech
    speech = text_to_speech.convert(search_result)

    return speech

# Create the Gradio interface
gr.Interface(fn=generate_output, inputs="audio", outputs="audio").launch()