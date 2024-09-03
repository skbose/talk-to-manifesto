from typing_extensions import override
from openai import OpenAI, AssistantEventHandler
from assistant import Assistant
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
            message_content.value = message_content.value.replace(
                annotation.text,""
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = self.client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        self.output = message_content.value
        # print(message_content.value)
        # print("\n".join(citations))
        

class TextToTextSearch:   
    def __init__(self, assistant):
        
        self.assistant = assistant        
        self.thread = self.assistant.client.beta.threads.create()
        
    def search(self, query):
        thread_message = self.assistant.client.beta.threads.messages.create(
            self.thread.id,
            role="user",
            content=query + "Return an elaborate answer in marathi without any format."#"आगामी निवडणुकीत तुम्ही कोणती प्रमुख आश्वासने देत आहात? थोडक्यात सांगा.",
            )
        with self.assistant.client.beta.threads.runs.stream(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            event_handler=EventHandler(self.assistant.client)) as stream:
            
            stream.until_done()
            return stream.output


# Example usage in main.py
if __name__ == "__main__":
    text = "आगामी निवडणुकीत तुम्ही कोणती प्रमुख आश्वासने देत आहात? थोडक्यात सांगा."
    client = OpenAI(api_key="sk-proj-SIqFozom657b2RQcIbvrT3BlbkFJpk5EZPznzgSLcfmjk0DX")
    assistant = Assistant(["माझा वचननामा.docx"], 
                          client, 
                          "menifesto", 
                          "marathi_menifesto_interpreter",
                          "तुम्हाला एका राजकारण्याचा वचननामा  दिला जातो. आता जनता तुम्हाला प्रश्न विचारेल आणि दिलेल्या वचननाम्याच्या आधारे तुम्हाला त्यांची उत्तरे द्यावी लागतील.",
                          "gpt-4o"
                          )
    print("assistant created")
    # wait = input("press enter to continue")
    search_tool = TextToTextSearch(assistant)
    results = search_tool.search(text)
    print(results)
