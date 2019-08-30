import os

from flask import request, jsonify

from src import *
from src.helper import image_utils
from src.helper.response_maker import make_response
from src.helper.timer import Timer
from src.torch.run import instance_segmentation_api


def post():
    try:
        body = request.json

        with Timer('Validate input data'):
            required_parameters = ['objects']
            if not all(x in body for x in required_parameters):
                return jsonify(make_response(True, message=f'{required_parameters} body parameters are required.')), 400

            if not all(o in COCO_INSTANCE_CATEGORY_NAMES for o in body['objects']):
                return jsonify(make_response(True, message='One or more objects from the list will not be detected.')), 400

            if bool('image_url' in body) == bool('image_base64' in body):
                return jsonify(make_response(True, message='image_url (x)or image_base64 has to be specified')), 400

            if 'return_bounding_box' not in body:
                body['return_bounding_box'] = False
            if 'return_text' not in body:
                body['return_text'] = False
            if 'return_white_bg' not in body:
                body['return_white_bg'] = False

        with Timer('Download image'):
            if 'image_url' in body:
                image_path = image_utils.download(body['image_url'])
            elif 'image_base64' in body:
                image_path = image_utils.decode(body['image_base64'])
            else:
                image_path = None

            if not image_path:
                return jsonify(make_response(True, message='Wrong image specified.')), 400

        with Timer('Generate image'):
            output_image_path = instance_segmentation_api(
                image_path, body['objects'], body['return_bounding_box'], body['return_text']
            )

        with Timer('Removing white color'):
            if not body['return_white_bg']:
                image_utils.remove_white(output_image_path)

        with Timer('Encoding image'):
            encoded_string = image_utils.encode(output_image_path)

        with Timer('Remove input and output images'):
            if os.path.exists(image_path):
                os.remove(image_path)
            if os.path.exists(output_image_path):
                os.remove(output_image_path)

        return jsonify(make_response(False, image_base64=encoded_string)), 200

    except Exception as e:
        return jsonify(make_response(True, message=f'Unexpected error: {e}')), 400
