import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from split_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from extract_markdown import extract_markdown_images, extract_markdown_links
from markdown_to_blocks import markdown_to_blocks, BlockType, block_to_block_type
from markdown_to_html_node import markdown_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("this", TextType.BOLD)
        node2 = TextNode("this", TextType.BOLD, TextType.LINK)
        self.assertNotEqual(node, node2)
    
    def test_this(self):
        node = TextNode("this", TextType.BOLD)
        node2 = TextNode("this", TextType.BOLD, url=None)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_split_nodes_code(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.PLAIN_TEXT
        )

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result, [
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN_TEXT),
        ])

    def test_split_nodes_no_delimiter(self):
        node = TextNode("Just plain text", TextType.PLAIN_TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result, [node])

    def test_split_nodes_unclosed_delimiter(self):
        node = TextNode("This is `broken code", TextType.PLAIN_TEXT)

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
             [
                 TextNode("This is text with a link ", TextType.PLAIN_TEXT),
                 TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                 TextNode(" and ", TextType.PLAIN_TEXT),
                 TextNode(
                     "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                 ),
             ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        result = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN_TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN_TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN_TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN_TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            result,
        )


        def test_markdown_to_blocks(self):
            md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
            """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )


        def test_block_to_block_type_heading(self):
            block = "### Hello world"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        def test_block_to_block_type_code_block(self):
            block = "```\nprint('hi')\n```"
            self.assertEqual(block_to_block_type(block), BlockType.CODE)

        def test_block_to_block_type_quote_block(self):
            block = "> Quote line 1\n>Quote line 2\n> Quote line 3"
            self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        def test_block_to_block_type_unordered_list(self):
            block = "- item 1\n- item 2\n- item 3"
            self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        def test_block_to_block_type_ordered_list(self):
            block = "1. first\n2. second\n3. third"
            self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        def test_block_to_block_type_ordered_list_not_starting_at_one(self):
            block = "2. second\n3. third"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        def test_block_to_block_type_ordered_list_not_incrementing(self):
            block = "1. first\n3. third"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        def test_headings(self):
            md = """
        # Heading 1

        ## Heading 2 with **bold**

        ###### Heading 6 with _italic_ and `code`
        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div>"
                "<h1>Heading 1</h1>"
                "<h2>Heading 2 with <b>bold</b></h2>"
                "<h6>Heading 6 with <i>italic</i> and <code>code</code></h6>"
                "</div>",
            )


        def test_quote_blocks(self):
            md = """
        > This is a quote with **bold**
        > and a second line with _italic_ and `code`
        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><blockquote>This is a quote with <b>bold</b>\nand a second line with <i>italic</i> and <code>code</code>\n</blockquote></div>",
            )


        def test_unordered_list(self):
            md = """
        - first **bold**
        - second _italic_
        - third `code`
        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ul>"
                "<li>first <b>bold</b></li>"
                "<li>second <i>italic</i></li>"
                "<li>third <code>code</code></li>"
                "</ul></div>",
            )


        def test_ordered_list(self):
            md = """
        1. first **bold**
        2. second _italic_
        3. third `code`
        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ol>"
                "<li>first <b>bold</b></li>"
                "<li>second <i>italic</i></li>"
                "<li>third <code>code</code></li>"
                "</ol></div>",
            )


        def test_paragraphs(self):
            md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )

        def test_codeblock(self):
            md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )


if __name__ == "__main__":
    unittest.main()
