import os
import shutil
import logging

from src.markdown_blocks import extract_title, markdown_to_html_node

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
    from_path: str,
    template_path: str,
    dest_path: str,
):
    logger.info(
        f"🛠️ Generating page from {from_path} to {dest_path} using {template_path}"
    )

    # Read Makrdown file
    with open(from_path, "r", encoding="utf-8") as file:
        markdown = file.read()
    title = extract_title(markdown)

    # Convert Markdown to HTML
    html_string = markdown_to_html_node(markdown).to_html()

    # Read Template file
    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()

    # Replace placeholders
    final_html = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_string
    )

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write to destination file
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(final_html)

    logger.info(f"✅ Page generated successfully: {dest_path}")


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
):
    """
    Recursively generate HTML pages from markdown files found in the content directory
    and write them to the public directory, maintaining the same directory structure.
    """

    # Iterate through all items in the content directory
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            # Only process markdown files
            if file.endswith(".md"):
                # Construct the full path to the markdown file
                markdown_file_path = os.path.join(root, file)

                # Determine the relative path of the markdown file
                relative_path = os.path.relpath(root, dir_path_content)

                # Construct the destination path in the public directory
                dest_dir = os.path.join(dest_dir_path, relative_path)

                # Ensure the destination directory exists
                os.makedirs(dest_dir, exist_ok=True)

                # Generate the destination path from the HTML file
                html_file_name = file.replace(".md", ".html")
                dest_path = os.path.join(dest_dir, html_file_name)

                # Generate the page using the generate_page function
                generate_page(markdown_file_path, template_path, dest_path)
