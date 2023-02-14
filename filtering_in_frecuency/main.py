import cv2
import numpy as np
import matplotlib.pyplot as plt

def low_pass_filter(rows,cols):
    center_row = int(rows/2)
    center_cols = int(cols/2)
    #mask = np.zeros((rows,cols))
    
    x = np.linspace(0, cols, cols)- center_cols
    y = np.linspace(0, rows, rows) -center_row
    xv, yv = np.meshgrid(x, y)
    #print(xv, yv)
    
    return xv**2 + yv**2 < 150**2
    

if __name__=='__main__':
    
    # Load the two images
    img = cv2.imread("city.jpg",0)
    img = cv2.resize(img, (500,300))
    
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)    
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    
    h,w =  img.shape
    mask = low_pass_filter(h,w)
    #print(mask[])
    
    
    fshift = np.multiply(fshift,mask) 
    
    f_ishift = np.fft.ifftshift(fshift)
    
    img_back = np.fft.ifft2(f_ishift)
    print(img_back.shape)
    img_back = np.abs(img_back)
    
    #print(type(img_back))
    #print(img_back.shape)
    plt.imshow(mask, cmap = 'gray')
    plt.show()
    plt.imshow(img_back, cmap = 'gray')
    plt.show()
    #cv2.imshow("img", img)


    #cv2.waitKey(0)
    #cv2.destroyAllWindows()