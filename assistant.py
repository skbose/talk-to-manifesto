from openai import OpenAI 
class Assistant:
    def __init__(self, text_file_paths, openai_client, vector_store_name, assistant_name, assistant_instructions, assistant_model):
        self.client = openai_client
        self.vector_store = self.client.beta.vector_stores.create(name=vector_store_name)
        file_streams = [open(path, "rb") for path in text_file_paths]
        file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=self.vector_store.id, files=file_streams)
        
        
        self.assistant = self.client.beta.assistants.create(
            name=assistant_name,
            instructions=assistant_instructions,
            model=assistant_model,
            tools=[{"type": "file_search"}],
            tool_resources={"file_search": {"vector_store_ids": [self.vector_store.id]}},
        )
        
        self.id = self.assistant.id
        

# Example usage in main.py
if __name__ == "__main__":
    text = """
    This is an example text file.
    It contains some text that we can search through.
    We will search for specific words in this text.
    """
    client = OpenAI(api_key="")
    assistant = Assistant(["माझा वचननामा.docx"], 
                          client, 
                          "menifesto", 
                          "marathi_menifesto_interpreter",
                          "तुम्हाला एका राजकारण्याचा वचननामा  दिला जातो. आता जनता तुम्हाला प्रश्न विचारेल आणि दिलेल्या वचननाम्याच्या आधारे तुम्हाला त्यांची उत्तरे द्यावी लागतील.",
                          "gpt-4o"
                          )
