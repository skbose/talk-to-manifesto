import logging
import os
import threading
from queue import Queue

import dotenv
import gradio as gr

from ai_hub.modules.ir_agent.search_rag import SearchRagOpenAI
from ai_hub.modules.stt.openai_stt import OpenAIStt
from ai_hub.modules.tts.hf_tts import HuggingFaceTTS
from ai_hub.modules.utils import save_wav_file

logging.basicConfig(level=logging.INFO)
dotenv.load_dotenv(override=True)


search_rag = SearchRagOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
tts = HuggingFaceTTS(url=os.getenv("HF_TTS_URL"), token=os.getenv("HF_TOKEN"))
stt = OpenAIStt(api_key=os.getenv("OPENAI_API_KEY"))

# create a queue to store the sentences
sentence_to_process = Queue()
sentence_processed = Queue()
lock = threading.Lock()

TEMPORARY_AUDIO_DIR = "audio_dir"


def rag_task(search_text: str):
    streaming_results = search_rag.search(search_text, stream_output=True)
    sentence_buffer = ""
    sentence_count = 0
    for result in streaming_results:
        if result.endswith((".", "!", "?")):
            with lock:
                sentence_to_process.put(sentence_buffer)
            sentence_buffer = ""
            sentence_count += 1
        else:
            sentence_buffer += result
    with lock:
        if sentence_buffer:
            sentence_to_process.put(sentence_buffer)
            sentence_count += 1

    logging.info(f"RAG task completed. {sentence_count} sentences processed")


def tts_task(rag_thread: threading.Thread):
    filename_idx = 0

    # create temporary audio directory
    os.makedirs(TEMPORARY_AUDIO_DIR, exist_ok=True)

    while sentence_to_process.qsize() > 0 or rag_thread.is_alive():
        if sentence_to_process.qsize() > 0:
            with lock:
                sentence = sentence_to_process.get()
            audio_output = tts.synthesize(sentence)
            if audio_output:
                tts.save_audio(
                    audio=audio_output["audio"],
                    filename=f"{filename_idx}.wav",
                    sampling_rate=audio_output["sampling_rate"],
                    output_dir=TEMPORARY_AUDIO_DIR,
                )
                with lock:
                    sentence_processed.put(
                        os.path.join(TEMPORARY_AUDIO_DIR, f"{filename_idx}.wav")
                    )
                filename_idx += 1
                logging.info(f"Generated audio for: {sentence}")
    logging.info("TTS task completed")
    logging.info(f"Sentence queue size: {sentence_to_process.qsize()}")
    logging.info(f"Sentence processed queue size: {sentence_processed.qsize()}")


def generate_audio_output(tts_thread: threading.Thread, sentence_processed: Queue):
    while tts_thread.is_alive() or sentence_processed.qsize() > 0:
        with lock:
            if sentence_processed.qsize() > 0:
                audio_file_name = sentence_processed.get()
                yield audio_file_name


def process_audio(audio):
    sr, raw = audio
    print(sr, raw.shape)
    # save as a wav file
    save_wav_file(raw, "input.wav", sr, TEMPORARY_AUDIO_DIR)
    input_audio_path = os.path.join(TEMPORARY_AUDIO_DIR, "input.wav")

    transcript = stt.extract_text(input_audio_path)
    logging.info(f"Transcription: {transcript}")

    import threading

    # Start rag_task in a separate thread
    rag_thread = threading.Thread(target=rag_task, args=(transcript,))
    rag_thread.start()

    # Start tts_task in a separate thread
    tts_thread = threading.Thread(target=tts_task, args=(rag_thread,))
    tts_thread.start()

    yield from generate_audio_output(tts_thread, sentence_processed)


with gr.Blocks() as demo:
    # add a box to record audio as input
    input_audio = gr.Audio(elem_id="input_audio", sources="microphone")
    stream_as_file_btn = gr.Button("मला उत्तर दे")
    stream_as_file_output = gr.Audio(
        streaming=True, elem_id="stream_as_file_output", autoplay=True
    )

    stream_as_file_btn.click(process_audio, input_audio, stream_as_file_output)


if __name__ == "__main__":
    demo.launch(
        server_name=os.getenv("GRADIO_SERVER_IP"),
        server_port=os.getenv("GRADIO_SERVER_PORT"),
    )
