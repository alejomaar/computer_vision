import matplotlib.pyplot as plt
import numpy as np

def show_images(img:np.ndarray, magnitude_spectrum:np.ndarray, filtered_img:np.ndarray)->None:
    plt.subplot(131), plt.imshow(img, cmap='gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(132), plt.imshow(magnitude_spectrum, cmap='gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.subplot(133), plt.imshow(filtered_img, cmap='gray')
    plt.title('Filtered Image'), plt.xticks([]), plt.yticks([])
    plt.show()