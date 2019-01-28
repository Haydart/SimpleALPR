import os

import cv2
from PIL import Image
from pytesseract import pytesseract

from util.basic_transformations import BasicTransformations
from util.image_display_helper import ImageDisplayHelper


def process_image(image):
    binarized_image = bt.otsu_threshold(image)
    config = '-l eng --oem 1 --psm 10'
    print(pytesseract.image_to_data(Image.fromarray(binarized_image), config=config))


if __name__ == '__main__':
    dh = ImageDisplayHelper(True, 2, 20)
    bt = BasicTransformations(dh)
    print(pytesseract.get_tesseract_version())
    dir_path = 'dataset/ocr_ready'
    for filename in os.listdir(dir_path):
        if any(filename.endswith(ext) for ext in ['.jpg', '.png', '.jpeg']):
            if filename.startswith('ocr'):
                print('\n Processing file {}'.format(filename))
                image = cv2.imread('{}/{}'.format(dir_path, filename))

    dh.plot_results()


def read_text(image_path):
    print(pytesseract.image_to_data(Image.open(image_path)))
