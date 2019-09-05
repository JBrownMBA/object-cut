import requests
import argparse

from src import *
from src.helper import image_utils


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_url', type=str)
    parser.add_argument('--image_path', type=str)
    parser.add_argument('--list', help='Add a list of desired classes', nargs='+', type=str, required=True)
    parser.add_argument('--return_white_bg', action='store_true')
    return parser.parse_args()


def test():
    if bool(args.image_url) == bool(args.image_path):
        print('image_url x(or) has to be specified.')
        return

    request_body = dict(
        objects=args.list,
        return_white_bg=args.return_white_bg
    )
    if args.image_url:
        request_body['image_url'] = args.image_url
    else:
        request_body['image_base64'] = image_utils.encode(args.image_path)
    endpoint_url = f'https://{PRODUCTION_SERVER_IP}/cut'
    response = requests.post(endpoint_url, json=request_body, timeout=60)
    if response.ok:
        response_json = response.json()
        output_path = image_utils.decode(response_json['response']['image_base64'])
        print(output_path)
    else:
        print(response.content)


if __name__ == '__main__':
    args = _parse_args()
    test()
