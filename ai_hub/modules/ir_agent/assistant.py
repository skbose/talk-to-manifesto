from openai import OpenAI


class Assistant:
    def __init__(
        self,
        text_file_paths: list[str],
        openai_client: OpenAI,
        vector_store_name: str,
        assistant_name: str,
        assistant_instructions: str,
        assistant_model: str,
    ):
        self.client = openai_client
        self.vector_store = self.client.beta.vector_stores.create(
            name=vector_store_name
        )
        file_streams = [open(path, "rb") for path in text_file_paths]
        self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=self.vector_store.id, files=file_streams
        )

        self.assistant = self.client.beta.assistants.create(
            name=assistant_name,
            instructions=assistant_instructions,
            model=assistant_model,
            tools=[{"type": "file_search"}],
            tool_resources={
                "file_search": {"vector_store_ids": [self.vector_store.id]}
            },
        )

        self.id = self.assistant.id
