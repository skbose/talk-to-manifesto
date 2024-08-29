class TextToTextSearch:
    def __init__(self, text):
        self.text = text

    def search(self, query):
        results = []
        for line in self.text.split('\n'):
            if query in line:
                results.append(line)
        return results
    

# Example usage in main.py
if __name__ == "__main__":
    text = """
    This is an example text file.
    It contains some text that we can search through.
    We will search for specific words in this text.
    """
    text_search = TextToTextSearch(text)
    results = text_search.search("search")