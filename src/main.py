from src.script import copy_static, logger, generate_page

dir_path_static = "./static"
dir_path_public = "./public"

page_dir_from = "./content/index.md"
template_path = "./template.html"
page_dir_to = "./public/index.html"


def main():

    logger.info("Starting static file copy process")
    copy_static(dir_path_static, dir_path_public)
    logger.info("Static file copy completed")

    generate_page(page_dir_from, template_path, page_dir_to)


if __name__ == "__main__":
    main()
