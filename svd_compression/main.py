import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
from cv2 import VideoWriter, VideoWriter_fourcc

#Image
#https://www.pexels.com/photo/close-up-photo-of-lion-s-head-2220336/

def create_video(width, height):
    FPS = 3
    fourcc = VideoWriter_fourcc(*'MP42')
    video = VideoWriter('./svd_compression.avi', fourcc, float(FPS), (width, height))
    return video

def svd_compression_animation(img):
    B = img[:,:,0] 
    G = img[:,:,1]
    R = img[:,:,2] 
    
    R_U, R_S, R_VT = np.linalg.svd(R,full_matrices=False)
    G_U, G_S, G_VT = np.linalg.svd(G,full_matrices=False)
    B_U, B_S, B_VT = np.linalg.svd(B,full_matrices=False)
    
    height,width, = R.shape[0], R.shape[1]
    
    max_rank = min(height, width)
    
    compression_range = [0,0.02,0.03,0.05,0.08,0.10,0.12,0.14,0.16,0.18,0.20,0.24,0.28,0.35,0.4,0.45,0.5,0.6,0.7,0.8,0.9,1]

    video = create_video(width, height)
    
    
    for compression_rate in compression_range:        

        r=int(compression_rate* max_rank )
        print(f'compression rate: {round(compression_rate,3)} - rank {r} of {max_rank} ')   
    
        R_compressed = img_approx_compressed(R_U, R_S, R_VT, r)
        G_compressed = img_approx_compressed(G_U, G_S, G_VT, r)
        B_compressed = img_approx_compressed(B_U, B_S, B_VT, r)
            
        img_compressed = cv2.merge([B_compressed, G_compressed,  R_compressed]) 

        video.write(img_compressed)
    
    video.release()
    
def svd_compression(img,r=10):
    
    B = img[:,:,0].astype(np.float32) 
    G = img[:,:,1].astype(np.float32) 
    R = img[:,:,2].astype(np.float32) 
    
    B_U, B_S, B_VT = np.linalg.svd(B,full_matrices=False)
    R_U, R_S, R_VT = np.linalg.svd(R,full_matrices=False)
    G_U, G_S, G_VT = np.linalg.svd(G,full_matrices=False)
        
    R_compressed = img_approx_compressed(R_U, R_S, R_VT, r)
    G_compressed = img_approx_compressed(G_U, G_S, G_VT, r)
    B_compressed = img_approx_compressed(B_U, B_S, B_VT, r)
    
    img_compressed = cv2.merge([B_compressed, G_compressed,  R_compressed])

    cv2.imshow('SVD: compression image',img_compressed)

   
    
def img_approx_compressed(U, S, VT, k):
    return np.clip((U[:,:k] @ np.diag(S[:k])) @ VT[:k],0,255).round().astype('uint8')

if __name__=='__main__':
    image = cv2.imread('camels.jpg')
    #image = cv2.resize(image,(0, 0), fx = 0.2, fy = 0.2)
    svd_compression_animation(image)
    
    

    cv2.waitKey(0)
    cv2.destroyAllWindows()