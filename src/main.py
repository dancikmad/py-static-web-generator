import sys
from src.script import copy_static, logger, generate_pages_recursive

basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

dir_path_static = "./static"
dir_path_public = "./docs"

content_dir = "./content"
template_path = "./template.html"


def main():

    # Copy static files to public directory
    logger.info("Starting static file copy process")
    copy_static(dir_path_static, dir_path_public)
    logger.info("Static file copy completed")

    # Generate all pages recursively from markdown files
    logger.info("Starting recursive page generation...")
    generate_pages_recursive(content_dir, template_path, dir_path_public, basepath)
    logger.info("Recursive page generation completed.")


if __name__ == "__main__":
    main()
