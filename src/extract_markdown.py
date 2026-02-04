import re

def extract_title(markdown):
    lines = markdown.split('\n')

    for line in lines:
        if line.startswith('# '):
            return line[1:].strip()

    raise Exception("No H1 header found in the provided markdown.")


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches

