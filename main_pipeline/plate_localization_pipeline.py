import argparse
import sys
from copy import copy

import util.band_clipping as bc
import util.bounding_boxes as bb
import util.heuristics as heuristics
import util.input_output as io
from main_pipeline.candidates import Candidates
from util.basic_transformations import BasicTransformations
from util.image_display_helper import ImageDisplayHelper
from util.pipeline_transformations import PipelineTransformations
from util.vehicles_detection import VehiclesDetector
import main_pipeline.plate_deskewing_pipeline as pdp
import util.utils as ut

image_helper = ImageDisplayHelper(True, subplot_width=2, subplot_height=10)
transformations = PipelineTransformations(BasicTransformations(image_helper))
vehicle_detector = VehiclesDetector()


def main(argv):
    args = parse()

    img_loader = io.BatchImageLoader()
    img_saver = io.ImageSaver(args.output_dir)

    for image in img_loader.load_images(args.input_dir):
        orginal_image = copy(image.image)
        counter = 0
        for sub_image in vehicle_detector.detect_vehicles(image.image):
            image.image = sub_image
            candidates = process(image.image)

            orginal = image.image
            image_boxes = apply_bounding_boxex(image.image, candidates)
            image.image = image_boxes
            img_saver.save_image(image, counter)
            counter = counter + 1
            image.image = orginal

            numrows = len(image.image)
            numcols = len(image.image[0])

            candidates_filtered = filter_heuristically(candidates.all, (numrows, numcols))
            image_boxes = bounding_box_filtered(image.image, candidates_filtered)

            image.image = image_boxes
            img_saver.save_image(image, counter)
            counter = counter + 1

            for idx, bond in enumerate(candidates_filtered):
                y0, y1, x0, x1 = bond
                print( idx, y0, y1, x0, x1)
                # ut.show_one_image(orginal_image[y0:y1, x0:x1])
                # deskewed = pdp.process_image(orginal_image[y0:y1, x0:x1])

                # ut.show_one_image(deskewed)
                # ocr_file = 'to_ocr{}.jpg'.format(idx)
                # # cv2.imwrite(ocr_file, deskewed)
                # ocr.read_text(ocr_file)

            image_helper.plot_results()
            image_helper.reset_subplot()


def parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', action='store', dest='input_dir', required=True, type=str)
    parser.add_argument('-o', action='store', dest='output_dir', required=True, type=str)

    return parser.parse_args()


def process(image):
    working_image = copy(image)
    working_image = transformations.preprocess(working_image)

    vert_sobel_image, hor_sobel_image = transformations.apply_skeletonized_sobel(copy(working_image))
    opening_method_image = transformations.apply_morph_opening(copy(working_image))
    color_method_image = transformations.apply_color_masks(copy(image))

    try:
        sobel_candidates = bc.find_candidates(bc.sobel_method, vert_sobel_image, hor_sobel_image)
    except ValueError:
        sobel_candidates = []

    try:
        opening_candidates = bc.find_candidates(bc.opening_method, opening_method_image)
    except ValueError:
        opening_candidates = []

    color_candidates = []
    for image_color in color_method_image:
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
    image_helper.add_to_plot(image_boxes, title='Final candidates')
    return image_boxes


def bounding_box_filtered(image, candidates_filtered):
    image_boxes = copy(image)
    image_boxes = bb.apply_bounding_boxes(image_boxes, candidates_filtered, bb.PINK)
    return image_boxes


def filter_heuristically(candidates, image_size):
    candidates = heuristics.remove_big_areas(candidates, image_size)
    candidates = heuristics.remove_vertical(candidates)
    candidates = heuristics.remove_horizontal(candidates, image_size[1])
    candidates = heuristics.join_separated_2(candidates)
    return candidates


if __name__ == '__main__':
    main(sys.argv)
