import numpy as np
from .fft import apply_fft,apply_ifft
from .low_pass import LowPass
from .high_pass import HighPass
import cv2



def get_filter(img:np.ndarray, is_high_pass:bool, filter_type:str, **kwargs):
    """
    Returns the filter for a given image, filter type, and parameters.
    
    Parameters:
        img (numpy.ndarray): Input image.
        is_high_pass (bool): Whether to apply a high-pass filter instead of a low-pass filter.
        filter_type (str): Type of filter to apply ("ideal", "gaussian", or "butterworth").
        **kwargs: Additional arguments required to construct the filter.
    
    Returns:
        numpy.ndarray: Filter.
    """
    rows, cols = img.shape
    if is_high_pass:
        filter = HighPass(rows, cols) 
    else:
        filter = LowPass(rows, cols)

    if filter_type == "ideal":
        low_pass_filter = filter.ideal(**kwargs)
    elif filter_type == "gaussiano":
        low_pass_filter = filter.gaussian(**kwargs)
    elif filter_type == "butterworth":
        low_pass_filter = filter.butterworth(**kwargs)
    else:
        raise ValueError("No valid filter type")

    return low_pass_filter

def apply_filter(img:np.ndarray, is_high_pass:bool, filter_type:str, filter_params:dict):
    """
    Applies a filter to the input image and returns the filtered image and frequency domain representation.
    
    Parameters:
        img (numpy.ndarray): Input image.
        is_high_pass (bool): Whether to apply a high-pass filter instead of a low-pass filter.
        filter_type (str): Type of filter to apply ("ideal", "gaussian", or "butterworth").
        filter_params (dict): Dictionary of filter parameters.
    
    Returns:
        tuple: The filtered image and filter
    """
    
    # Compute the 2D Fourier transform of the image
    fshift = apply_fft(img)

    # Obtain the filter
    filter = get_filter(img, is_high_pass, filter_type, **filter_params)

    # Apply the filter to the spectrum
    filtered_spectrum = np.multiply(fshift, filter)
    fft_mag_log = np.log(abs(filtered_spectrum+1))
    # Compute the inverse Fourier transform to obtain the filtered image
    filtered_img = apply_ifft(filtered_spectrum)
    
    return filtered_img,fft_mag_log 

    
def apply_low_pass(img:np.ndarray, filter_type:str, filter_params:dict):
    """ Applies a low-pass filter to the input image and returns the filtered image
    """    
    return apply_filter(img,False, filter_type, filter_params)

def apply_high_pass(img:np.ndarray, filter_type:str, filter_params:dict):
    """ Applies a high-pass filter to the input image and returns the filtered image
    """   
    return apply_filter(img,True, filter_type, filter_params)