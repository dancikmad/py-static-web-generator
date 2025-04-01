import os
import shutil
import logging
import re


# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def copy_static(source_dir: str, dest_dir: str):
    """
    Recursively copy files from source_dir to dest_dir.
    If dest_dir exists, it will be deleted first.
    """
    # Delete destination directory if it exists
    if os.path.exists(dest_dir):
        logger.info(f"Removing existing directory: {dest_dir}")
        shutil.rmtree(dest_dir)

    # Create destination directory
    logger.info(f"Creating directory: {dest_dir}")
    os.makedirs(dest_dir)

    # Copy files and subdirectories recursively
    copy_files_recursive(source_dir, dest_dir)


def copy_files_recursive(source_dir: str, dest_dir: str):
    """
    Helper function that recursively copies files from source_dir to dest_dir
    """

    # Get all items in the source directory
    items = os.listdir(source_dir)

    for item in items:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        # If item is a file, copy it
        if os.path.isfile(source_path):
            logger.info(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)

        # If item is a directory, create it and copy its contents recursively
        elif os.path.isdir(source_path):
            logger.info(f"Creating directory: {dest_path}")
            os.makedirs(dest_path, exist_ok=True)
            copy_files_recursive(source_path, dest_path)


def generate_page(
    content_path: str, template_path: str, output_path: str, basepath: str
):
    # Ensure basepath ends with "/"
    if not basepath.endswith("/"):
        basepath += "/"

    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()

    with open(content_path, "r", encoding="utf-8") as content_file:
        content = content_file.read()

    # Replace placeholders
    page_content = template.replace(
        "{{ Title }}", os.path.basename(content_path).replace(".md", "")
    )
    page_content = page_content.replace("{{ Content }}", content)

    # Replace href/src paths correctly
    page_content = re.sub(r'href="/([^"]*)"', rf'href="{basepath}\1"', page_content)
    page_content = re.sub(r'src="/([^"]*)"', rf'src="{basepath}\1"', page_content)

    # Write the final output
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(page_content)


def generate_pages_recursive(
    content_dir: str, template_path: str, output_dir: str, basepath: str
):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(content_dir):
        input_path = os.path.join(content_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(".md", ".html"))

        if os.path.isdir(input_path):
            generate_pages_recursive(input_path, template_path, output_path, basepath)
        else:
            generate_page(input_path, template_path, output_path, basepath)
