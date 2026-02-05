from markdown_to_html_node import markdown_to_html_node
from htmlnode import HTMLNode
from extract_markdown import extract_title
import os
from pathlib import Path


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        from_path_contents = file.read()

    with open(template_path, "r") as file:
        from_template_contents = file.read()

    html_node = markdown_to_html_node(from_path_contents).to_html()

    title = extract_title(markdown=from_path_contents)

    full_html = from_template_contents.replace("{{ Title }}", title).replace("{{ Content }}", html_node)

    full_html = (
        full_html
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )

    dest_dir_name = os.path.dirname(dest_path)

    os.makedirs(dest_dir_name, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(full_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)





