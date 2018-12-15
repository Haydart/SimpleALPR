from utils import *

if __name__ == '__main__':
    image = load_image('./license_plate_snapshots/test_079.jpg')
    # image = imutils.resize(image, width=512)

    grayscale_image = gray_scale(image)
    plot_image(grayscale_image, 1, 'Original image grayscale')
    plot_image(grayscale_image, 2, 'Original image grayscale BGR', fix_colors=False)
    plot_image(canny_edge_detection(grayscale_image), 3, 'Canny on original image')

    noise_removed_image = bilateral_filter(grayscale_image)
    plot_image(noise_removed_image, 4, 'Bilateral filtering')

    noise_removed_image = bilateral_filter(grayscale_image)
    plot_image(noise_removed_image, 5, 'Bilateral filtering BGR', fix_colors=False)
    vertical_image = vertical_detection(noise_removed_image)
    print(vertical_image.channels())
    img = cv2.adaptiveThreshold(vertical_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    plot_image(img, 6, 'Vertical after bilateral')

    histogram_equalized_image = histogram_equalization(noise_removed_image)
    plot_image(histogram_equalized_image, 7, 'Histogram equalization')
    plot_image(histogram_equalized_image, 8, 'Histogram equalization BGR', fix_colors=False)
    plot_image(canny_edge_detection(histogram_equalized_image), 9, 'Canny after histogram equalization')

    subtracted_image = morphological_opening(histogram_equalized_image)
    plot_image(subtracted_image, 10, 'Opening subtracted')
    plot_image(subtracted_image, 11, 'Opening subtracted BGR', fix_colors=False)
    plot_image(canny_edge_detection(subtracted_image), 12, 'Canny after opening subtraction')

    plt.subplots_adjust(bottom=0.1, left=0.1, right=0.9, top=0.9, wspace=0.3, hspace=0.3)

    fig = plt.gcf()
    fig.set_size_inches(10, 15)

    print('calculated')

    plt.show()
