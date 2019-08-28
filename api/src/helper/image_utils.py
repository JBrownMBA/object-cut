import uuid
import base64
import requests
from PIL import Image
from src import *


def download(image_url):
    output_path = None
    response = requests.get(image_url, timeout=15)
    if response.ok:
        output_path = f'{DATA_FOLDER}/{uuid.uuid4()}.png'
        with open(output_path, 'wb') as f:
            f.write(response.content)
    return output_path


def decode(image_base64):
    image_data = base64.b64decode(image_base64)
    output_path = f'{DATA_FOLDER}/{uuid.uuid4()}.png'
    with open(output_path, 'wb') as f:
        f.write(image_data)
    return output_path


def encode(output_image_path):
    with open(output_image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string


def is_white(r, g, b):
    if r == 255 and g == 255 and b == 255:
        return True
    else:
        return False


def remove_white(image_path):
    img = Image.open(image_path)
    img = img.convert('RGBA')
    pix_data = img.getdata()

    new_data = []
    for item in pix_data:
        if is_white(item[0], item[1], item[2]):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(image_path, "PNG", quality=95)
