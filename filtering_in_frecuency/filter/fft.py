import numpy as np



def meshgrid(rows,cols):
    """
    Create a mesh grid of coordinates centered around the center.

    Returns
    -------
    xv, yv : 2D arrays
        Arrays containing the x and y coordinates of the mesh grid.

    """
    center_row = int(rows/2)
    center_cols = int(cols/2)
    
    x = np.linspace(0, cols,cols)- center_cols
    y = np.linspace(0, rows, rows) -center_row
    xv, yv = np.meshgrid(x, y)
    return xv, yv

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