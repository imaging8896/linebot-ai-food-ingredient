import io
import os

from PIL import Image

from .logging import logger


def save_image_to_file(image_bytes: bytearray, file_path: str):
    logger.info(f"Saving image {len(image_bytes)=} to {file_path}")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(image_bytes)

def compressed_image_bytes(image_bytes: bytearray):
    logger.info(f"Compressing image {len(image_bytes)=}")
    # Use PIL to compress the image
    try:
        image = Image.open(io.BytesIO(image_bytes))

        cur_size = image.width + image.height
        if cur_size > 1600:
            resize_ratio = 1600 / cur_size
            new_width = int(image.width * resize_ratio)
            new_height = int(image.height * resize_ratio)
            image = image.resize((new_width, new_height))

        output = io.BytesIO()
        image.save(output, format='JPEG', quality=60, optimize=True)
        compressed_bytes = bytearray(output.getvalue())
        logger.info(f"Compressed image {len(compressed_bytes)=}")
        return compressed_bytes
    except Exception:
        logger.exception("Failed to compress image")
        return image_bytes

def remove_images(image_prefix: str, remove_folder: str):
    logger.info(f"Removing images with prefix {image_prefix} from folder {remove_folder}")
    for file_or_dir in os.listdir(remove_folder):
        file_or_dir_path = os.path.join(remove_folder, file_or_dir)
        if file_or_dir.startswith(image_prefix) and os.path.isfile(file_or_dir_path):
            logger.info(f"Removing image file {file_or_dir_path}")
            os.remove(file_or_dir_path)
