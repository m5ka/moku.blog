from io import BytesIO

from django.core.files import File
from PIL import Image


def _convert_image_to_webp(image_file):
    image = Image.open(image_file)
    image.convert("RGB")
    image.thumbnail((486, 486))
    thumb_io = BytesIO()
    image.save(thumb_io, "WEBP")
    return File(thumb_io, name=image_file.name)


def process_avatar_image(image_file):
    return _convert_image_to_webp(image_file)


def process_post_image(image_file):
    return _convert_image_to_webp(image_file)
