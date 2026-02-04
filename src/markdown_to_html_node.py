from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from split_delimiter import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown=markdown)
    print(blocks)#['This is **bolded** paragraph\ntext in a p\ntag here', 'This is another paragraph with _italic_ text and `code` here']

    block_nodes = []

    for block in blocks:
        type_of_block = block_to_block_type(markdown_block=block)
        print(type_of_block)#BlockType.PARAGRAPH
        
        if type_of_block == BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            children = text_to_children(block)
            block_nodes.append(ParentNode(tag="p", children=children))

        elif type_of_block == BlockType.QUOTE:
            cleaned = strip_quote_markers(block)
            children = text_to_children(cleaned)
            block_nodes.append(ParentNode(tag="blockquote", children=children))

        elif type_of_block == BlockType.HEADING:
            level = heading_level(block)

            cleaned = block[level:]
            if cleaned.startswith(" "):
                cleaned = cleaned[1:]
            cleaned = cleaned.strip()

            children = text_to_children(cleaned)
            block_nodes.append(ParentNode(tag=f"h{level}", children=children))

        elif type_of_block == BlockType.CODE:
            # Strip ``` fences
            lines = block.split("\n")
            code_text = "\n".join(lines[1:-1])

            # Create <code> node (no inline parsing!)
            code_node = LeafNode(
                tag="code",
                value=code_text
            )

            # Wrap in <pre>
            pre_node = ParentNode(
                tag="pre",
                children=[code_node]
            )

            block_nodes.append(pre_node)

        elif type_of_block == BlockType.UNORDERED_LIST:
            items = unordered_list_items(block)

            li_nodes = []
            for item in items:
                children = text_to_children(item)          # inline parsing allowed
                li_nodes.append(ParentNode(tag="li", children=children))

            block_nodes.append(ParentNode(tag="ul", children=li_nodes))


        elif type_of_block == BlockType.ORDERED_LIST:
            items = ordered_list_items(block)

            li_nodes = []
            for item in items:
                children = text_to_children(item)          # inline parsing allowed
                li_nodes.append(ParentNode(tag="li", children=children))

            block_nodes.append(ParentNode(tag="ol", children=li_nodes))



            

    return ParentNode(tag="div", children=block_nodes)


def text_to_children(text):
    result = []
    nodes = text_to_textnodes(text)

    for node in nodes:
        result.append(text_node_to_html_node(node))

    return result


def heading_level(line):
    i = 0
    while i < len(line) and line[i] == "#":
        i += 1
    return i


def strip_quote_markers(block: str) -> str:
    lines = block.split("\n")
    cleaned_lines = []

    for line in lines:
        if line.startswith("> "):
            cleaned_lines.append(line[2:])
        elif line.startswith(">"):
            cleaned_lines.append(line[1:])
        else:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def unordered_list_items(block: str) -> list[str]:
    items = []
    for line in block.split("\n"):
        line = line.strip()
        if not line:
            continue

        # remove marker: "- ", "* ", "+ "
        if line.startswith(("- ", "* ", "+ ")):
            items.append(line[2:].strip())
        else:
            # if your block_to_block_type is correct, this shouldn't happen,
            # but it's safe to include
            items.append(line)
    return items


def ordered_list_items(block: str) -> list[str]:
    items = []
    for line in block.split("\n"):
        line = line.strip()
        if not line:
            continue

        # find "N. " prefix
        i = 0
        while i < len(line) and line[i].isdigit():
            i += 1

        # if we have digits then ". " remove that prefix
        if i > 0 and i + 1 < len(line) and line[i] == "." and line[i + 1] == " ":
            items.append(line[i + 2:].strip())
        else:
            # fallback
            items.append(line)
    return items
