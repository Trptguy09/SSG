import os
import shutil


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
        if stripped.startswith('# ') and not stripped.startswith('##'):
            return stripped[2:].strip()
    else:
        raise Exception("No h1 title found")

def generate_page(from_path, template_path, dest_path):
    from_path =  
    



def main():

    src_dir = "static"
    dst_dir = "public"

    print(f"Starting copy from '{src_dir}' to '{dst_dir}")
    copy_recursive(src_dir, dst_dir)


if __name__ == "__main__":
    main()
