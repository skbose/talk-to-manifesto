import gradio as gr
from speech_to_text import SpeechToText
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
speech_to_text = SpeechToText()
text_to_text_search = TextToTextSearch(assistant=assistant)
text_to_speech = TextToSpeech()

# Define the Gradio interface
def generate_output(sound):
    # audio is a tuple with the first element as sample rate and the second as the audio data
    original_sample_rate, data = sound

    # Target sample rate
    target_sample_rate = 16000

    # Resample the audio data if the original sample rate is different
    if original_sample_rate != target_sample_rate:
        number_of_samples = round(len(data) * target_sample_rate / original_sample_rate)
        data = resample(data, number_of_samples)

    # Ensure data is in int16 format (common format for WAV files)
    data = np.asarray(data, dtype=np.int16)
    
    print("writing file")

    # Save the resampled audio
    filename = "output_16000.wav"
    wavfile.write(filename, target_sample_rate, data)
    
    print("file written")
    text = speech_to_text.convert_audio_to_text(filename)
    
    print(f"text converted from audio. Converted text is: {text}")
    # Search for relevant text
    search_result = text_to_text_search.search(text)
    
    print(f"search result: {search_result}")

    # Convert search result to speech
    speech = text_to_speech.convert(search_result, return_speech = False)
    return search_result, (speech["sampling_rate"], np.array(speech["audio"][0]))

# Create the Gradio interface
gr.Interface(fn=generate_output, inputs="audio", outputs=["text","audio"]).launch()

# Create Gradio interface
iface = gr.Interface(
    fn=generate_output, 
    inputs=gr.Audio(type="numpy"), 
    outputs=["text","audio"],
    title="Record and Save Audio",
    description="Record audio and save it as a WAV file with a sample rate of 16,000 Hz."
)

# Launch the interface
iface.launch()
