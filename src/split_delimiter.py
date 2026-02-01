from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links


def text_to_textnodes(text):
    node = TextNode(text=text, text_type=TextType.PLAIN_TEXT)
    
    code_node = split_nodes_delimiter([node], "`", TextType.CODE)

    bold_node = split_nodes_delimiter(code_node, "**", TextType.BOLD)

    italics_node = split_nodes_delimiter(bold_node, "_", TextType.ITALIC)

    image_node = split_nodes_image(italics_node)

    link_node = split_nodes_link(image_node)

    return link_node

    


def has_closing_delimiter(text, delimiter):
    return text.count(delimiter) % 2 == 0

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # Only split plain text nodes; leave others untouched
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        text = node.text

        # If delimiter exists, it must be balanced
        if not has_closing_delimiter(text, delimiter):
            raise ValueError(f"Unclosed delimiter '{delimiter}' in: {text}")

        # If delimiter not present, keep as-is
        if delimiter not in text:
            new_nodes.append(node)
            continue

        parts = text.split(delimiter)

        for i, part in enumerate(parts):
            if part == "":
                # Optional: skip empty segments created by consecutive delimiters
                continue

            if i % 2 == 0:
                # outside delimiters -> plain text
                new_nodes.append(TextNode(part, TextType.PLAIN_TEXT))
            else:
                # inside delimiters -> requested type
                new_nodes.append(TextNode(part, text_type))

    return new_nodes
    


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)

        if len(matches) == 0:
            new_nodes.append(node)
            continue

        original_text = node.text

        for match in matches:
            image_alt = match[0]
            image_link = match[1]

            sections = original_text.split(f"![{image_alt}]({image_link})", 1)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN_TEXT))

    return new_nodes



def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)

        if len(matches) == 0:
            new_nodes.append(node)
            continue

        original_text = node.text

        for match in matches:
            link_alt = match[0]
            url_link = match[1]

            sections = original_text.split(f"[{link_alt}]({url_link})", 1)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))

            new_nodes.append(TextNode(link_alt, TextType.LINK, url_link))

            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN_TEXT))

    return new_nodes



