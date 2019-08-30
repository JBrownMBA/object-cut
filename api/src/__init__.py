COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
    'traffic light', 'fire hydrant', 'N/A', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
    'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A', 'handbag',
    'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
    'skateboard', 'surfboard', 'tennis racket', 'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
    'couch', 'potted plant', 'bed', 'N/A', 'dining table', 'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse',
    'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book', 'clock',
    'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

MODEL_THRESHOLD = 0.5
MODEL_RECT_TH = 3
MODEL_TEXT_SIZE = 3
MODEL_TEXT_TH = 3

IMAGE_DIMENSIONS_PIXELS = (512, 512)
PIX_TO_INCH = 0.0104166667
DATA_FOLDER = 'data'
PRODUCTION_SERVER_IP = '134.209.244.212:8083'

__all__ = [
    'COCO_INSTANCE_CATEGORY_NAMES',
    'MODEL_THRESHOLD',
    'MODEL_RECT_TH',
    'MODEL_TEXT_SIZE',
    'MODEL_TEXT_TH',
    'IMAGE_DIMENSIONS_PIXELS',
    'PIX_TO_INCH',
    'DATA_FOLDER',
    'PRODUCTION_SERVER_IP'
]
