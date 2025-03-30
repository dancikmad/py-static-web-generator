from script import copy_static, logger

dir_path_static = "./static"
dir_path_public = "./public"


def main():

    logger.info("Starting static file copy process")
    copy_static(dir_path_static, dir_path_public)
    logger.info("Static file copy completed")


if __name__ == "__main__":
    main()
