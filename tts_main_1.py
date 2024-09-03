import gradio as gr
from text_to_speech import TextToSpeech
import numpy as np
import scipy
from openai import OpenAI
from assistant import Assistant
from text_to_text_search import TextToTextSearch


text_to_speech = TextToSpeech()


client = OpenAI(api_key="sk-proj-SIqFozom657b2RQcIbvrT3BlbkFJpk5EZPznzgSLcfmjk0DX")
assistant = Assistant(["/Users/skbose/Downloads/manifesto.docx"], 
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


def stream_audio(text):
    i = 0
    search_result = text_to_text_search.search(text)

    print ("GPT Response:", search_result)

    # Create a pause audio sample
    pause_duration = 0.5  # Duration of pause in seconds
    sample_rate = 16000  # Standard sample rate
    pause_samples = int(pause_duration * sample_rate)
    pause_audio = np.zeros(pause_samples, dtype=np.int16)
    
    for speech in text_to_speech.convert_stream(search_result):
        i += 1
        file = f"{i}.wav"
        # Convert the audio to 16-bit integer
        # Convert the audio to 16-bit integer
        audio_int16 = np.int16(speech["audio"][0] / np.max(np.abs(speech["audio"][0])) * 32767)
        
        # Append the pause audio to the speech audio
        combined_audio = np.concatenate((audio_int16, pause_audio))
        # Write the WAV file
        scipy.io.wavfile.write(
            file,
            rate=speech["sampling_rate"],
            data=combined_audio
        )
        yield file
        

with gr.Blocks() as demo:
    input_text = gr.Textbox(lines=1, label="Convert Marathi Text to Speech - TTS Streaming")
    stream_as_file_btn = gr.Button("Generate Speech")
    stream_as_file_output = gr.Audio(streaming=True, elem_id="stream_as_file_output", autoplay=True)
    stream_as_file_btn.click(
        stream_audio, input_text, stream_as_file_output
    )

if __name__ == "__main__":
    demo.launch()
