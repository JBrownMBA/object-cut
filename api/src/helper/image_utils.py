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
    img = Image.open(output_path).convert('RGBA')
    img.save(output_path, format='PNG', quality=95)
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
    img.save(image_path, format='PNG', quality=95)


def get_resize_dimensions(original_size, dimensions):
    dim_x, dim_y = dimensions
    img_x, img_y = original_size
    if img_x >= img_y:
        return int(dim_x), int(img_y * (dim_x / (img_x * 1.0)))
    else:
        return int(img_x * (dim_y / (img_y * 1.0))), int(dim_y)


def resize_aspect(image, dimensions=IMAGE_DIMENSIONS_PIXELS, re_sample=Image.LANCZOS):
    new_dim = get_resize_dimensions(image.size, dimensions)
    if new_dim == image.size:
        return image.copy()
    else:
        return image.resize(size=new_dim, resample=re_sample)
