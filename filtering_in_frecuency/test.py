import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load the image and convert it to grayscale
img = cv2.imread('city.jpg', 0)

# Compute the 2D Fourier transform of the image
f = np.fft.fft2(img)

# Shift the zero-frequency component to the center of the spectrum
fshift = np.fft.fftshift(f)

# Compute the magnitude spectrum of the Fourier transform
magnitude_spectrum = 20*np.log(np.abs(fshift))

# Define the Gaussian filter
rows, cols = img.shape
crow, ccol = rows/2, cols/2
d = 30  # The cutoff frequency of the filter
gaussian_filter = np.zeros((rows, cols))
for i in range(rows):
    for j in range(cols):
        gaussian_filter[i,j] = np.exp(-((i-crow)**2 + (j-ccol)**2)/(2*d**2))

# Apply the Gaussian filter to the magnitude spectrum
filtered_spectrum = np.multiply(gaussian_filter, fshift)

# Shift the zero-frequency component back to the corner of the spectrum
filtered_spectrum_shift = np.fft.ifftshift(filtered_spectrum)

# Compute the inverse Fourier transform to obtain the filtered image
filtered_img = np.fft.ifft2(filtered_spectrum_shift)
filtered_img = np.abs(filtered_img)

# Display the original image and the filtered image
plt.subplot(131),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(132),plt.imshow(magnitude_spectrum, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.subplot(133),plt.imshow(filtered_img, cmap = 'gray')
plt.title('Filtered Image'), plt.xticks([]), plt.yticks([])
plt.show()