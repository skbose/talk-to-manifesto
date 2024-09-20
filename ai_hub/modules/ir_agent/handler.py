from openai import AssistantEventHandler
from typing_extensions import override


class EventHandler(AssistantEventHandler):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        self.output = ""

    @override
    def on_message_done(self, message) -> None:
        # print a citation to the file searched
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(annotation.text, "")
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = self.client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        self.output = message_content.value
