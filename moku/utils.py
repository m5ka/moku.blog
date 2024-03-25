from io import BytesIO

from django.core.files import File
from emoji import demojize
from PIL import Image


def process_image(image_file):
    image = Image.open(image_file)
    image.convert("RGB")
    image.thumbnail((486, 486))
    thumb_io = BytesIO()
    image.save(thumb_io, "WEBP")
    return File(thumb_io, name=".".join(image_file.name.split(".")[:-1] + ["webp"]))


def unemoji(txt: str):
    return demojize(txt, delimiters=("", ""))
