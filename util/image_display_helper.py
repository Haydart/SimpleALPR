import cv2
import matplotlib as mpl

mpl.interactive(True)
mpl.rcParams['figure.dpi'] = 300
from matplotlib import pyplot as plt


class ImageDisplayHelper:
    subplot_width = None
    subplot_height = None
    subplot_index = 0
    pipeline_debug_enabled = False

    def __init__(self, debug_pipeline, subplot_width, subplot_height):
        self.subplot_width = subplot_width
        self.subplot_height = subplot_height
        self.pipeline_debug_enabled = debug_pipeline
        plt.figure("Pipeline", figsize=(30, 30))

    def reset_subplot(self):
        self.subplot_index = 0
        plt.gcf().clf()

    def add_to_plot(self, image, subplot_index=None, title='', fix_colors=True):
        if self.pipeline_debug_enabled:
            current_subplot_index = None
            if not subplot_index:
                self.subplot_index = self.subplot_index + 1
                current_subplot_index = self.subplot_index
            else:
                current_subplot_index = subplot_index

            try:
                plt.subplot(self.subplot_height, self.subplot_width, current_subplot_index)
            except SyntaxError:
                print("Please enlarge subplot space in image helper definition")

            if fix_colors:
                if len(image.shape) == 3 and image.shape[2] == 3:
                    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), aspect='auto')
                else:
                    plt.imshow(image, cmap='gray', aspect='auto')
            else:
                plt.imshow(image, aspect='auto')

            plt.title(title)
            plt.axis('off')

    def plot_results(self):
        if self.pipeline_debug_enabled:
            plt.subplots_adjust(bottom=0.1, left=0.02, right=0.75, top=0.98, wspace=1, hspace=1)
            fig = plt.gcf()
            fig.set_size_inches(5, 25)
            # plt.tight_layout()
            print('plot display')
            plt.show()

    def save_results(self, path):
        plt.savefig(path)
