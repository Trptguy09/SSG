import os
import shutil
from pathlib import Path

from markdown_to_blocks import markdown_to_html_node


def copy_recursive(src, dst):
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory not found: {src}")

    if os.path.exists(dst):
        shutil.rmtree(dst)
        print(f"Deleted contents of: {dst}")

    os.makedirs(dst)
    print(f"Created destination directory: {dst}")

    def recursive_copy(current_src, current_dst):
        for item in os.listdir(current_src):
            src_path = os.path.join(current_src, item)
            dst_path = os.path.join(current_dst, item)

            if os.path.isdir(src_path):
                os.makedirs(dst_path)
                print(f"Created directory: {dst_path}")
                recursive_copy(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
                print(f"Copied file: {src_path} to {dst_path}")

    recursive_copy(src, dst)
    print("Copy completed")


def extract_title(markdown):
    for line in markdown.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("# ") and not stripped.startswith("##"):
            return stripped[2:].strip()
    else:
        raise Exception("No h1 title found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    src = from_path.open().read()
    with template_path.open() as f:
        temp = f.read()
    src_html = markdown_to_html_node(src).to_html()
    title = extract_title(src)
    new_title = temp.replace("{{ Title }}", title)
    html_page = new_title.replace("{{ Content }}", src_html)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with dest_path.open("w") as f:
        f.write(html_page)


def main():

    src_dir = Path("static")
    dst_dir = Path("public")
    copy_recursive(src_dir, dst_dir)
    content_md = Path("content/index.md")
    template_file = Path("template.html")
    dest_file = dst_dir / "index.html"
    generate_page(content_md, template_file, dest_file)


if __name__ == "__main__":
    main()
