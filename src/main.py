import sys
from src.script import copy_static, logger, generate_pages_recursive

# Get basepath from command line arguments, default to "/"
basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

# Update output directory to docs instead of public
dir_path_static = "./static"
dir_path_output = "./docs"
content_dir = "./content"
template_path = "./template.html"


def main():
    # Copy static files to docs directory
    logger.info("Starting static file copy process")
    copy_static(dir_path_static, dir_path_output)
    logger.info("Static file copy completed")

    # Generate all pages recursively from markdown files
    logger.info("Starting recursive page generation...")
    generate_pages_recursive(content_dir, template_path, dir_path_output, basepath)
    logger.info("Recursive page generation completed.")


if __name__ == "__main__":
    main()
