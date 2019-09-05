import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
import torchvision.transforms as torch_transform

from PIL import Image

from src import *
from src.helper import image_utils
from src.helper.timer import Timer
from src.object_cut import model


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', type=str)
    parser.add_argument('--list', help='Add a list of desired classes', nargs='+', type=str, required=True)
    parser.add_argument('--remove_white', action='store_true')
    return parser.parse_args()


def _get_prediction(img_path, threshold):
    with Timer('Transform image'):
        with Image.open(img_path).convert('RGB') as img:
            img = image_utils.resize_aspect(img)
            img.save(img_path, format='JPEG', quality=95)
        transform = torch_transform.Compose([torch_transform.ToTensor()])
        img_transformed = transform(img)

    with Timer('Predict'):
        prediction = model([img_transformed])

    with Timer('Get results'):
        prediction_score = list(prediction[0]['scores'].detach().numpy())
        prediction_t = [prediction_score.index(x) for x in prediction_score if x > threshold][-1]
        masks = (prediction[0]['masks'] > 0.5).squeeze().detach().cpu().numpy()
        prediction_class = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(prediction[0]['labels'].numpy())]
        prediction_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(prediction[0]['boxes'].detach().numpy())]
        masks = masks[:prediction_t+1]
        prediction_boxes = prediction_boxes[:prediction_t+1]
        prediction_class = prediction_class[:prediction_t+1]

    return masks, prediction_boxes, prediction_class


def _random_colour_masks(image):
    r = np.zeros_like(image).astype(np.uint8)
    g = np.zeros_like(image).astype(np.uint8)
    b = np.zeros_like(image).astype(np.uint8)
    r[image == 0], g[image == 0], b[image == 0] = [255, 255, 255]
    coloured_mask = np.stack([r, g, b], axis=2)
    return coloured_mask


def instance_segmentation_api(image_path, object_list):
    masks, boxes, prediction_cls = _get_prediction(image_path, MODEL_THRESHOLD)

    with Timer('Apply mask'):
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if masks.any():
            rgb_mask_list = np.zeros(masks[0].shape)
            for i in range(len(masks)):
                if prediction_cls[i] in object_list:
                    rgb_mask_list += masks[i]
            rgb_mask = _random_colour_masks(rgb_mask_list)
            img = cv2.addWeighted(img, 1, rgb_mask, 1, 0)

    with Timer('Generate image result'):
        image_path_output = f'{".".join(image_path.split(".")[:-1])}_output.png'
        plt.figure(figsize=(img.shape[0] * PIX_TO_INCH, img.shape[1] * PIX_TO_INCH))
        plt.axis('off')
        plt.imshow(img)
        plt.savefig(image_path_output, bbox_inches='tight', dpi=175)
        del img

    return image_path_output


if __name__ == '__main__':
    args = _parse_args()
    output_image_path = instance_segmentation_api(args.image_path, args.list)
    if args.remove_white:
        image_utils.remove_white(output_image_path)
