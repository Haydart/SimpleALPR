import logging

import cv2
import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt

logger = logging.getLogger()
mpl.rcParams['figure.dpi'] = 150
subplot_width = 3
subplot_height = 5


def load_image(path):
    logger.info("Loading image from %s...", path)
    image = cv2.imread(path)
    return image


def plot(figure, subplot, image, title):
    figure.subplot(subplot)

    figure.imshow(image)
    figure.xlabel(title)
    figure.xticks([])
    figure.yticks([])
    return True


def plot_(figure, subplot, image, title):
    figure.subplot(subplot)

    figure.plot(image)
    figure.xlabel(title)
    figure.xticks([])
    figure.yticks([])
    return True


def plot_image(img, subplot_index, title='', fix_colors=True):
    plt.subplot(subplot_height, subplot_width, subplot_index)

    if fix_colors:
        if len(img.shape) == 3 and img.shape[2] == 3:
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        else:
            plt.imshow(img, cmap='gray')
    else:
        plt.imshow(img)

    plt.title(title)
    plt.axis('off')


def gray_scale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def bilateral_filter(image):
    return cv2.bilateralFilter(image, 32, 40, 40)


def histogram_equalization(image):
    return cv2.equalizeHist(image)


def morphological_opening(image, kernel_size=(3, 3), iterations=15):
    opening_mask = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    opening_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel=opening_mask, iterations=iterations)
    return cv2.subtract(image, opening_image)


def morphological_closing(image, kernel_size=(3, 3), iterations=6):
    kernel = np.ones(kernel_size, np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=iterations)


def erosion(image, kernel_size=(3, 3), iterations=1):
    kernel_size = np.ones(kernel_size, np.uint8)
    return cv2.erode(image, kernel_size, iterations=iterations)


def canny_edge_detection(image, low_thresh=170, high_thresh=200):
    return cv2.Canny(image, low_thresh, high_thresh)


def _normalize_sobel_to_cv8u(sobel_image):
    sobelx_64f = sobel_image - np.min(sobel_image)  # to have only positive values
    div = np.max(sobelx_64f) / 255  # calculate the normalize divisor
    sobel_8u = np.uint8(sobelx_64f / div)
    return sobel_8u


def sobel_vertical_edge_detection(image):
    vertical_image = cv2.Sobel(image, cv2.CV_32F, 1, 0, ksize=3)
    return _normalize_sobel_to_cv8u(vertical_image)


def sobel_horizontal_edge_detection(image):
    horizontal_image = cv2.Sobel(image, cv2.CV_32F, 0, 1, ksize=3)
    return _normalize_sobel_to_cv8u(horizontal_image)


def binary_threshold(image, thresh):
    _, threshed = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)
    return threshed


def skeletonization(image):
    size = np.size(image)
    skeleton = np.zeros(image.shape, np.uint8)

    # img = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 10)
    img = binary_threshold(image, 127)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    done = False

    while not done:
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skeleton = cv2.bitwise_or(skeleton, temp)
        img = eroded.copy()

        zeros = size - cv2.countNonZero(img)
        if zeros == size:
            done = True

    return skeleton


def show_results(original_image, gray_image, canny_image, auto_canny_image):
    plt.figure("test", figsize=(30, 30))
    plot(plt, 321, original_image, "Original image")
    plot(plt, 322, gray_image, "Canny image")
    plot(plt, 323, canny_image, "Y bound")
    plot(plt, 324, auto_canny_image, "X bound")

    plt.tight_layout()
    plt.show()

    return True


def plot_histograms(hist_1, hist_2, title):
    plt.figure("Histograms", figsize=(10, 5))
    plot_(plt, 121, hist_1, "Before")
    plot_(plt, 122, hist_2, "After")

    plt.title(title)
    plt.show()
