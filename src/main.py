from textnode import TextNode, TextType

def main():
    text_node_object = TextNode(text="This is some anchor text", text_type=TextType.LINK, url="https://www.boot.dev")
    print(text_node_object)

if __name__ == "__main__":
    main()
