import argparse
import sys
from copy import copy

import util.band_clipping as bc
import util.bounding_boxes as bb
import util.input_output as io
from main_pipeline.candidates import Candidates
from util.basic_transformations import BasicTransformations
from util.image_display_helper import ImageDisplayHelper
from util.pipeline_transformations import PipelineTransformations

image_helper = ImageDisplayHelper(True, 2, 15)
transformations = PipelineTransformations(BasicTransformations(image_helper))


def main(argv):
    args = parse()

    img_loader = io.BatchImageLoader()
    img_saver = io.ImageSaver(args.output_dir)

    for image in img_loader.load_images(args.input_dir):
        candidates = process(image.image)
        image_boxes = apply_bounding_boxex(image.image, candidates)

        image.image = image_boxes
        img_saver.save_image(image)
        image_helper.plot_results()
        image_helper.reset_subplot_index()


def parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', action='store', dest='input_dir', required=True, type=str)
    parser.add_argument('-o', action='store', dest='output_dir', required=True, type=str)

    return parser.parse_args()


def process(image):
    working_image = copy(image)
    working_image = transformations.preprocess(working_image)

    vert_sobel_image, hor_sobel_image = transformations.apply_skeletonized_sobel(copy(working_image))
    image_opening_method_image = transformations.apply_morph_opening(copy(working_image))
    images_color_method_image = transformations.apply_color_masks(copy(image))

    sobel_candidates = bc.find_candidates(bc.sobel_method, vert_sobel_image, hor_sobel_image)
    opening_candidates = bc.find_candidates(bc.opening_method, image_opening_method_image)

    color_candidates = []
    for image_color in images_color_method_image:
        try:
            candidates = bc.find_candidates(bc.color_method, image_color)
            color_candidates.extend(candidates)
        except ValueError:
            continue

    candidates = Candidates(
        sobel_candidates=sobel_candidates,
        opening_candidates=opening_candidates,
        color_candidates=color_candidates
    )
    return candidates


def apply_bounding_boxex(image, candidates):
    image_boxes = copy(image)
    image_boxes = bb.apply_bounding_boxes(image_boxes, candidates.sobel_candidates, bb.GREEN)
    image_boxes = bb.apply_bounding_boxes(image_boxes, candidates.opening_candidates, bb.RED)
    image_boxes = bb.apply_bounding_boxes(image_boxes, candidates.color_candidates, bb.BLUE)
    return image_boxes


if __name__ == '__main__':
    main(sys.argv)
