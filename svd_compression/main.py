import numpy as np
import cv2
import pandas as pd
from cv2 import VideoWriter, VideoWriter_fourcc
import matplotlib.pyplot as plt

def create_video(width, height,video_file='output.mp4'):
    FPS = 10
    fourcc = VideoWriter_fourcc(*'MP4V')
    video = VideoWriter(f'output/{video_file}', fourcc, float(FPS), (width, height))
    return video

def svd_compression_animation(img,output_name='output'):
    B = img[:,:,0] 
    G = img[:,:,1]
    R = img[:,:,2] 
    
    R_U, R_S, R_VT = np.linalg.svd(R,full_matrices=False)
    G_U, G_S, G_VT = np.linalg.svd(G,full_matrices=False)
    B_U, B_S, B_VT = np.linalg.svd(B,full_matrices=False)
    
    height,width, = R.shape[0], R.shape[1]
    
    max_rank = min(height, width)
    
    step=2
    
    stats(B_S,R_S,G_S,height,width,step=2, verbose=True,csv_filename=f'{output_name}.csv')
    
    rank_range = np.arange(1,  max_rank + 1,2)

    video = create_video(width, height,f'{output_name}.mp4')
    
    
    for rank in rank_range:        

        print(f'rank: {rank} - of {max_rank} ')   
    
        R_compressed = img_approx_compressed(R_U, R_S, R_VT, rank)
        G_compressed = img_approx_compressed(G_U, G_S, G_VT, rank)
        B_compressed = img_approx_compressed(B_U, B_S, B_VT, rank)
            
        img_compressed = cv2.merge([B_compressed, G_compressed,  R_compressed]) 

        video.write(img_compressed)
    
    video.release()
    
def svd_compression(img,compression_rate=0.5,output_name='output'):
    
    B = img[:,:,0].astype(np.float32) 
    G = img[:,:,1].astype(np.float32) 
    R = img[:,:,2].astype(np.float32) 
    
    B_U, B_S, B_VT = np.linalg.svd(B,full_matrices=False)
    R_U, R_S, R_VT = np.linalg.svd(R,full_matrices=False)
    G_U, G_S, G_VT = np.linalg.svd(G,full_matrices=False)
    
    height,width, = R.shape[0], R.shape[1]
    
    max_rank = min(height, width)
    
    low_rank=int(compression_rate* max_rank)
    
    #stats(B_S,R_S,G_S,height,width,step=2, verbose=True,csv_filename=f'{output_name}.csv')
        
    R_compressed = img_approx_compressed(R_U, R_S, R_VT, low_rank)
    G_compressed = img_approx_compressed(G_U, G_S, G_VT, low_rank)
    B_compressed = img_approx_compressed(B_U, B_S, B_VT, low_rank)
    
    img_compressed = cv2.merge([B_compressed, G_compressed,  R_compressed])

    cv2.imshow('SVD: compression image',img_compressed)
    

    
def stats(B_S,R_S,G_S,height,width,step=1,csv_filename='output.csv',verbose=True):
    #Sum singular values ranks of RGB channels
    S = np.array((B_S,R_S,G_S)).sum(axis=0)
    
    total_S = S.sum()
    n_components = len(S)
    rank_idx = np.arange(1,  n_components + 1)
    
    info_retained = 100 * np.cumsum(S) / total_S
    compression_ratio = height*width/(rank_idx*(height+width+1))
        
    df =pd.DataFrame({'rank':rank_idx,'info_retained':info_retained,'compression_ratio':compression_ratio})
    df =df[::step]
    df.to_csv(f'output/{csv_filename}',index=False)
    
    if(verbose==True):
        df.plot(x='rank',y=['info_retained','compression_ratio'])
        plt.grid(linestyle='--')
        plt.show()
    
    
    

    
def img_approx_compressed(U, S, VT, k):
    return np.clip((U[:,:k] @ np.diag(S[:k])) @ VT[:k],0,255).round().astype('uint8')

if __name__=='__main__':
    image = cv2.imread('img/landscape.jpg')
    
    '''
    Rescale the image for faster calculations
    '''
    #image = cv2.resize(image,None, fx = 0.5, fy = 0.5,interpolation=cv2.INTER_CUBIC)
    
    # * Execute this for animation
    svd_compression_animation(image,'landscape')
    
    # * Execute this for get only one svd image
    #svd_compression(image,0.1)
    
    

    cv2.waitKey(0)
    cv2.destroyAllWindows()