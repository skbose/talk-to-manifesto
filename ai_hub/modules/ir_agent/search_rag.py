import logging

from openai import OpenAI

from ai_hub.modules.ir_agent.assistant import Assistant
from ai_hub.modules.ir_agent.constants import (
    ASSISTANT_INSTRUCTIONS,
    ASSISTANT_MODEL,
    ASSISTANT_NAME,
    RESPONSE_FORMAT,
    TEXT_FILE_PATHS,
    VECTOR_STORE_NAME,
)
from ai_hub.modules.ir_agent.handler import EventHandler

logging.basicConfig(level=logging.INFO)


class SearchRagOpenAI:
    def __init__(self, api_key: str):
        self.openai_client = OpenAI(api_key=api_key)
        self.assistant = self._init_assistant()
        self.thread = self.assistant.client.beta.threads.create()

    def _init_assistant(self):
        return Assistant(
            text_file_paths=TEXT_FILE_PATHS,
            openai_client=self.openai_client,
            vector_store_name=VECTOR_STORE_NAME,
            assistant_name=ASSISTANT_NAME,
            assistant_instructions=ASSISTANT_INSTRUCTIONS,
            assistant_model=ASSISTANT_MODEL,
        )

    def search(self, query, stream_output=False):
        # create a message in the thread
        self.assistant.client.beta.threads.messages.create(
            self.thread.id, role="user", content=query + " " + RESPONSE_FORMAT
        )

        # create a run in the thread
        with self.assistant.client.beta.threads.runs.stream(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            event_handler=EventHandler(self.assistant.client),
        ) as stream:

            if stream_output:
                for event in stream:
                    if (
                        hasattr(event, "data")
                        and hasattr(event.data, "delta")
                        and hasattr(event.data.delta, "content")
                    ):
                        for content in event.data.delta.content:
                            if content.type == "text":
                                yield content.text.value
            else:
                stream.until_done()
                return stream.output


if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv(override=True)

    search_rag = SearchRagOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    search_text = "आगामी निवडणुकीत तुम्ही कोणती प्रमुख आश्वासने देत आहात? थोडक्यात सांगा."

    logging.info(f"Searching for: {search_text}")
    results = search_rag.search(search_text, stream_output=True)

    sentence_buffer = ""
    for result in results:
        # print(result, end="", flush=True)
        if result.endswith((".", "!", "?")):
            print("sentence", sentence_buffer)
            sentence_buffer = ""
        else:
            sentence_buffer += result
