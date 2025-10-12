import os

import requests

from .logging import logger


class UnableToFetchImageError(Exception):
    pass


def get_image_bytes(image_url: str, retry: int = 1) -> bytes:
    response = requests.get(image_url)
    if not response.ok:
        if retry > 0:
            logger.warning(f"Retrying to fetch image from {image_url}, {retry} retries left")
            return get_image_bytes(image_url, retry - 1)
        raise UnableToFetchImageError(f"Failed to fetch image from {image_url}")
    return response.content


def save_image_to_file(image_bytes: bytes, file_path: str):
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
