from textnode import TextNode, TextType
from copy_all_contents import copy_all_contents
from generate_page import generate_page, generate_pages_recursive
import os
import shutil
import sys

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

basepath = "/"
if len(sys.argv) > 1:
    basepath = sys.argv[1]

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    copy_all_contents(dir_path_static, dir_path_docs)

    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)

if __name__ == "__main__":
    main()
