import re


def split_into_lines(text: str):
    # This pattern splits the text at '.', '?', '!', but keeps the delimiter
    lines = re.split(r'(?<=[.?!])\s+', text.strip())
    lines = [line.strip() for line in lines if line]
    
    return lines
