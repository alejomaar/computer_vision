import cv2
from visualization import show_images
from preprocessing.filter import apply_high_pass
from constants import IDEAL_FILTER,GAUSSIAN_FILTER,BUTTERWORTH_FILTER


if __name__ == '__main__':
    # Read image   
    img = cv2.imread("img/city.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply high pass filter
    filter_type = IDEAL_FILTER
    filter_params = {"cutoff_frequency": 30}
    filtered_img, filtered_spectrum = apply_high_pass(img, filter_type, filter_params)
    
    show_images(img,filtered_img,filtered_spectrum)