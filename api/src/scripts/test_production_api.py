import requests
import argparse

from src import *
from src.helper import image_utils


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_url', type=str)
    parser.add_argument('--image_path', type=str)
    parser.add_argument('--list', help='Add a list of desired classes', nargs='+', type=str, required=True)
    return parser.parse_args()


def _print_args():
    print(f'[Image URL]: {args.image_url}')
    print(f'[Image path]: {args.image_path}')
    print(f'[Object list]: {args.list}')


def test():
    if bool(args.image_url) == bool(args.image_path):
        print('image_url x(or) has to be specified.')
        return

    if args.image_url:
        request_body = dict(objects=args.list, image_url=args.image_url)
    else:
        request_body = dict(objects=args.list, image_base64=image_utils.encode(args.image_path))
    endpoint_url = f'http://{PRODUCTION_SERVER_IP}/cut'
    response = requests.post(endpoint_url, json=request_body, timeout=60)
    if response.ok:
        response_json = response.json()
        output_path = image_utils.decode(response_json['response']['image_base64'])
        print(output_path)
    else:
        return response.content


if __name__ == '__main__':
    args = _parse_args()
    _print_args()
    test()
