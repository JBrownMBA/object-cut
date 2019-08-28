import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
import torchvision.transforms as torch_transform

from PIL import Image

from src import *
from src.helper import image_utils
from src.object_cut import model

args = None


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', type=str)
    parser.add_argument('--list', help='Add a list of desired classes', nargs='+', type=str, required=True)
    parser.add_argument('--bounding_box', action='store_true')
    parser.add_argument('--with_text', action='store_true')
    return parser.parse_args()


def _get_prediction(img_path, threshold):
    img = Image.open(img_path).convert('RGB')
    img = image_utils.resize_aspect(img)
    img.save(img_path, format='JPEG', quality=95)
    transform = torch_transform.Compose([torch_transform.ToTensor()])
    img = transform(img)
    prediction = model([img])
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


def instance_segmentation_api(image_path, object_list, threshold=0.5, rect_th=3, text_size=3, text_th=3):
    masks, boxes, prediction_cls = _get_prediction(image_path, threshold)
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if masks.any():
        rgb_mask_list = np.zeros(masks[0].shape)
        for i in range(len(masks)):
            if prediction_cls[i] in object_list:
                rgb_mask_list += masks[i]
                if args and args.bounding_box:
                    cv2.rectangle(img, boxes[i][0], boxes[i][1], color=(0, 255, 0), thickness=rect_th)
                if args and args.with_text:
                    cv2.putText(
                        img, prediction_cls[i], boxes[i][0], cv2.FONT_HERSHEY_SIMPLEX,
                        text_size, (0, 255, 0), thickness=text_th
                    )
        rgb_mask = _random_colour_masks(rgb_mask_list)
        img = cv2.addWeighted(img, 1, rgb_mask, 1, 0)
    image_path_output = f'{".".join(image_path.split(".")[:-1])}_output.png'
    plt.figure(figsize=(img.shape[0] * PIX_TO_INCH, img.shape[1] * PIX_TO_INCH))
    plt.axis('off')
    plt.imshow(img)
    plt.savefig(image_path_output, bbox_inches='tight', dpi=175)
    return image_path_output


if __name__ == '__main__':
    args = _parse_args()
    output_image_path = instance_segmentation_api(args.image_path, args.list)
    image_utils.remove_white(output_image_path)
