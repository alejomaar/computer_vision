import cv2
from visualization import show_images
from preprocessing.filter import apply_high_pass
from constants import IDEAL_FILTER,GAUSSIAN_FILTER,BUTTERWORTH_FILTER

"""This Python code reads an image, converts it to grayscale, and applies a high pass filter on it.
The high pass filter can be of three types: IDEAL_FILTER,GAUSSIAN_FILTER,BUTTERWORTH_FILTER.
You can increase the cutoff frequency, the higher it is, the sharper the image will be with much more defined edges.
The filtered image and its spectrum are then displayed using the visualization function 'show_images'
"""

if __name__ == '__main__':
    # Read image   
    img = cv2.imread("img/lenna.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Prompt user for filter type
    filter_choice = input("Enter filter type (ideal, gaussian, butterworth): ")
    
    # Select the low pass filter
    if filter_choice == 'ideal':
        filter_type = IDEAL_FILTER
        filter_params = {"cutoff_frequency": 30}
    elif filter_choice == 'gaussian':
        filter_type = GAUSSIAN_FILTER
        filter_params = {"cutoff_frequency": 30}
    else:
        filter_type = BUTTERWORTH_FILTER
        filter_params = {"cutoff_frequency": 30,'degree': 2}
        
    filtered_img, filtered_spectrum = apply_high_pass(img, filter_type, filter_params)
    
    show_images(img,filtered_spectrum,filtered_img)