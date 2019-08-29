import argparse
import warnings
import numpy as np

from PIL import Image


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--images', nargs='+', type=str, required=True)
    return parser.parse_args()


def combine():
    assert len(args.images) > 0

    images = [Image.open(i).convert('RGBA') for i in args.images]
    min_shape = sorted([(np.sum(i.size), i.size) for i in images])[0][1]
    images_combined = np.hstack((np.asarray(i.resize(min_shape)) for i in images))

    images_combined = Image.fromarray(images_combined)
    images_combined.save(f'{".".join(args.images[0].split(".")[:-1])}_combined.png')


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    args = _parse_args()
    combine()
