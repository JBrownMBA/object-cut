import uuid
import base64
import requests

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
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string
