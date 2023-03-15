import cv2
from visualization import show_images
from preprocessing.filter import apply_low_pass
from constants import IDEAL_FILTER,GAUSSIAN_FILTER,BUTTERWORTH_FILTER

"""This Python code reads an image, converts it to grayscale, and applies a low pass filter on it.
The low pass filter can be of three types: IDEAL_FILTER,GAUSSIAN_FILTER,BUTTERWORTH_FILTER.
You can increase the cutoff frequency, the higher it is, the smoothing in the image will be much more slight.
The filtered image and its spectrum are then displayed using the visualization function 'show_images'
"""

if __name__ == '__main__':
    # Read image   
    img = cv2.imread("img/city.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply low pass filter
    filter_type = GAUSSIAN_FILTER
    filter_params = {"cutoff_frequency": 30}
    filtered_img, filtered_spectrum = apply_low_pass(img, filter_type, filter_params)
    
    show_images(img,filtered_img,filtered_spectrum)