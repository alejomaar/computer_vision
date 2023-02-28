import cv2
import matplotlib.pyplot as plt
import numpy as np
from visualization import show_images
from filter.filter import apply_low_pass


if __name__ == '__main__':
    # Read image   
    img = cv2.imread("city.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (500, 300)) 
    
    # Aplicar el filtro de paso bajo con una frecuencia de corte de 30 Hz
    filter_type = "gaussiano"
    filter_params = {"cutoff_frequency": 30}
    filtered_img, filtered_spectrum = apply_low_pass(img, filter_type, filter_params)
    
    show_images(img,filtered_img,filtered_spectrum)