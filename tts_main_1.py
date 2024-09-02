import gradio as gr
from text_to_speech import TextToSpeech
import numpy as np

text_to_speech = TextToSpeech()

def stream_audio(text):
    i = 0
    for speech in text_to_speech.convert(text):
        i += 1
        file = f"{i}.wav"
        # Convert the audio to 16-bit integer
        audio_int16 = np.int16(speech["audio"][0] / np.max(np.abs(speech["audio"][0])) * 32767)
        # Write the WAV file
        scipy.io.wavfile.write(
            file,
            rate=speech["sampling_rate"],
            data=audio_int16
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
