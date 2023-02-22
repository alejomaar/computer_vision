import cv2
import numpy as np
import matplotlib.pyplot as plt
from filter.low_pass import LowPass
from filter.high_pass import HighPass
from enum import Enum

#Complementary resource: https://www.dsi.unive.it/~bergamasco/teachingfiles/cvslides/5_filtering_in_frequency_domain.pdf

class FrecuencyFilteringMode(Enum):
    LOW_PASS = LowPass
    HIGH_PASS = HighPass
    
class Filter(Enum):
    IDEAL = 'IDEAL'
    GAUSSIAN = 'GAUSSIAN'
    BUTTERWORTH = 'BUTTERWORTH'
    
class FilterParameters(Enum):
    IDEAL = {'cutoff_frequency':100}
    GAUSSIAN = {'cutoff_frequency':100}
    BUTTERWORTH = {'cutoff_frequency':100,'degree':8}
   
def apply_fft(img: np.ndarray)-> np.ndarray:
    """
    Computes the 2D Fourier transform of the image.

    Args:
        img: The input image.

    Returns:
        The shifted frequency domain representation of the image.
    """
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)    
    return fshift

def apply_ifft(fshift: np.ndarray) -> np.ndarray:
    """
    Computes the inverse Fourier transform to obtain the filtered image.

    Args:
        fshift: The shifted frequency domain representation of the image.

    Returns:
        The filtered image.
    """
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    return img_back

def get_filter_mode(filter_mode:str,rows: int,cols: int):
    """
    Returns the filter mode instance based on the input filter mode.

    Args:
        filter_mode: The type of filter mode.
        rows: The number of rows of the input image.
        cols: The number of columns of the input image.

    Returns:
        The filter mode instance.
    """
    if(filter_mode== FrecuencyFilteringMode.LOW_PASS):
        return LowPass(rows,cols)
    elif(filter_mode== FrecuencyFilteringMode.HIGH_PASS):
        return HighPass(rows,cols)
    else:
        raise Exception("Sorry, no FrecuencyFilteringMode type available")
    
def get_filter(filter_mode,filter_type,**kwargs)->np.ndarray:
    """
    Returns the filter in frecuency domain based on the input filter type.

    Args:
        filter_mode: The frequency filtering mode (Low pass or High Pass).
        filter_type: The type of filter.
        **kwargs: Additional arguments to pass to the filter constructor.

    Returns:
        The filter in frecuency domain.
    """    
    if(filter_type== Filter.IDEAL):
        return filter_mode.ideal(**kwargs)
    elif(filter_type== Filter.GAUSSIAN):
        return filter_mode.gaussian(**kwargs)
    elif(filter_type== Filter.BUTTERWORTH):
        return filter_mode.butterworth(**kwargs)
    else:
        raise Exception("Sorry, no filter available")
    
def show_images(img:np.ndarray, frecuency_filter:np.ndarray, filtered_img:np.ndarray)->None:
    plt.subplot(131), plt.imshow(img, cmap='gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(132), plt.imshow(frecuency_filter, cmap='gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.subplot(133), plt.imshow(filtered_img, cmap='gray')
    plt.title('Filtered Image'), plt.xticks([]), plt.yticks([])
    plt.show()

def apply_frequency_filter(img:np.ndarray, filter_mode_option:str, filter_type_option:str, filter_params:dict):
    """Main function to read image, apply frequency filter and display results"""
    # Compute the 2D Fourier transform of the image   
    fshift = apply_fft(img)
    
    # Define the filter
    rows, cols = img.shape
    filter_mode = get_filter_mode(filter_mode_option, rows, cols) ##low or high pass filter
    frequency_filter = get_filter(filter_mode, filter_type_option, **filter_params) 
    
    # Apply the filter to the magnitude spectrum    
    filtered_spectrum = np.multiply(fshift, frequency_filter) 
    
    # Compute the inverse Fourier transform to obtain the filtered image
    filtered_img = apply_ifft(filtered_spectrum)
    
    # Display the original image and the filtered image
    show_images(img,frequency_filter,filtered_img)

if __name__ == '__main__':
    # Read image   
    img = cv2.imread("city.jpg", 0)
    img = cv2.resize(img, (500, 300)) 
    
    #Select if you want LOW PASS or HIGH PASS filter
    frecuency_filtering_mode = FrecuencyFilteringMode.LOW_PASS
    #Select the filter (BUTTERWORTH,IDEAL,GAUSSIAN) 
    filter_chosen = Filter.IDEAL  
    #Bind filter parameters 
    #(Change the default values in FilterParameters or assign a dictionary with the parameters directly)
    params =  FilterParameters[filter_chosen.value].value
    
    print(f'Apply {filter_chosen.name} {frecuency_filtering_mode.name} filter with params: {params}')
    
    apply_frequency_filter(img,frecuency_filtering_mode,filter_chosen,params)
    




