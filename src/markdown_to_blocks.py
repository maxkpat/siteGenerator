from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown_block):
    lines = markdown_block.split("\n")

    #Code block
    if (
        markdown_block.startswith("```\n")
        and markdown_block.endswith("\n```")
    ):
        return BlockType.CODE

    #Heading
    if re.match(r"^#{1,6} ", markdown_block):
        return BlockType.HEADING

    #Quote
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    #Unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    #Ordered list
    is_ordered = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            is_ordered = False
            break

    if is_ordered:
        return BlockType.ORDERED_LIST

    #Default
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split("\n\n") if block.strip()]

    return blocks

