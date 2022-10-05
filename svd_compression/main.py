import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
from cv2 import VideoWriter, VideoWriter_fourcc

def create_video(width, height):
    FPS = 0.5
    fourcc = VideoWriter_fourcc(*'MP42')
    video = VideoWriter('./svd_compression.avi', fourcc, float(FPS), (width, height))
    return video

def svd_compression(img):
    B = img[:,:,0] / 255
    G = img[:,:,1] / 255
    R = img[:,:,2] / 255
    
    R_U, R_S, R_VT = np.linalg.svd(R)
    G_U, G_S, G_VT = np.linalg.svd(G)
    B_U, B_S, B_VT = np.linalg.svd(B)
    
    height,width, = R.shape[0], R.shape[1]
    
    compression_range = np.linspace(0, 1, num=45)
    
    video = create_video(width, height)
    
    max_rank = min(height, width)
    
    for compression_rate in compression_range:        

        r=int(compression_rate* max_rank )
        print(f'compression rate: {round(compression_rate,3)} - rank {r} of {max_rank} ')   
    
        R_compressed = img_approx_compressed(R_U, R_S, R_VT, r)
        G_compressed = img_approx_compressed(G_U, G_S, G_VT, r)
        B_compressed = img_approx_compressed(B_U, B_S, B_VT, r)
    
        img_compressed_float = np.dstack((B_compressed,G_compressed,R_compressed))
        img_compressed = (img_compressed_float*255).astype(np.uint8)
        
        video.write(img_compressed)
    
    video.release()
    
    
    return img_compressed
    
    
    
def img_approx_compressed(U, S, VT, k):
    return (U[:,:k] @ np.diag(S[:k])) @ VT[:k]

if __name__=='__main__':
    image = cv2.imread('camels.jpg')
    image = cv2.resize(image,(0, 0), fx = 0.3, fy = 0.3)
    svd_compression(image) 

    cv2.waitKey(0)
    cv2.destroyAllWindows()