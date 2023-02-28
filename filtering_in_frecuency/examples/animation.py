import cv2
from filter.filter import apply_high_pass
from cv2 import VideoWriter, VideoWriter_fourcc

def create_video(width, height,video_file='output.mp4'):
    FPS = 8
    fourcc = VideoWriter_fourcc(*'mp4v')
    video = VideoWriter(f'{video_file}', fourcc, float(FPS), (width, height))
    return video

if __name__ == '__main__':
    # Read image   
    img = cv2.imread("city.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (500, 300)) 
    
    filter_type = "gaussiano"
    h, w = img.shape
    
    video = create_video(w,h,f'video.mp4')
    #Create a video for multiple cuttof frequency
    for cutoff_frequency in range(5,150,3):
        filter_params = {"cutoff_frequency": cutoff_frequency}
        filtered_img, filtered_spectrum = apply_high_pass(img, filter_type, filter_params)
        backtorgb = cv2.cvtColor(filtered_img,cv2.COLOR_GRAY2RGB) 
        #push frame
        video.write(backtorgb)
    #export video 
    video.release()
