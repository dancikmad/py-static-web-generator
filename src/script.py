import os
import shutil
import logging

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
