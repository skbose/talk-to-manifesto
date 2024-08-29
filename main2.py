import gradio as gr
from text_to_text_search import TextToTextSearch
from text_to_speech import TextToSpeech
from openai import OpenAI
from assistant import Assistant
import numpy as np
import soundfile as sf
from scipy.signal import resample
import scipy.io.wavfile as wavfile

client = OpenAI(api_key="sk-proj-SIqFozom657b2RQcIbvrT3BlbkFJpk5EZPznzgSLcfmjk0DX")
assistant = Assistant(["माझा वचननामा.docx"], 
                      client, 
                      "menifesto", 
                      "marathi_menifesto_interpreter",
                      "तुम्हाला एका राजकारण्याचा वचननामा  दिला जातो. आता जनता तुम्हाला प्रश्न विचारेल आणि दिलेल्या वचननाम्याच्या आधारे तुम्हाला त्यांची उत्तरे द्यावी लागतील.",
                      'gpt-3.5-turbo',
                    )
print("assistant created")
# Initialize the three main classes
text_to_text_search = TextToTextSearch(assistant=assistant)
text_to_speech = TextToSpeech()

# Define the Gradio interface
def generate_output(text):
    # audio is a tuple with the first element as sample rate and the second as the audio data
    search_result = text_to_text_search.search(text)
    
    print(f"search result: {search_result}")

    # Convert search result to speech
    speech = text_to_speech.convert(search_result, return_speech = False)
    return search_result, (speech["sampling_rate"], np.array(speech["audio"][0]))


# Create Gradio interface
iface = gr.Interface(
    fn=generate_output, 
    inputs="text", 
    outputs=["text","audio"],
    title="Record and Save Audio",
    description="Record audio and save it as a WAV file with a sample rate of 16,000 Hz."
)

# Launch the interface
iface.launch()
