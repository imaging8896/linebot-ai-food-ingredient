import os

from .logging import logger


def save_image_to_file(image_bytes: bytearray, file_path: str):
    logger.info(f"Saving image {len(image_bytes)=} to {file_path}")
    with open(file_path, "wb") as f:
        f.write(image_bytes)


def remove_images(image_prefix: str, remove_folder: str):
    logger.info(f"Removing images with prefix {image_prefix} from folder {remove_folder}")
    for file_or_dir in os.listdir(remove_folder):
        file_or_dir_path = os.path.join(remove_folder, file_or_dir)
        if file_or_dir.startswith(image_prefix) and os.path.isfile(file_or_dir_path):
            logger.info(f"Removing image file {file_or_dir_path}")
            os.remove(file_or_dir_path)
