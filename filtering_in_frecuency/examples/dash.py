import cv2
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import base64
import numpy as np

from preprocessing.filter import apply_low_pass
from preprocessing.fft import apply_fft
from constants import IDEAL_FILTER,GAUSSIAN_FILTER,BUTTERWORTH_FILTER

# Define constants
IMG_FILE = 'img/city.png'
FILTER_TYPE = BUTTERWORTH_FILTER
CUTOFF_FREQUENCIES = list(range(10, 100, 5))
ANIMATION_INTERVAL = 200

def load_image(file_path: str) -> np.ndarray:
    """Load an image from a file."""
    img = cv2.imread(file_path, 0)
    if img is None:
        raise ValueError(f"Failed to load image from file: {file_path}")
    return img

def full_log_magnitude(img):
    fshift = apply_fft(img)
    fft_mag_log = 20*np.log(abs(fshift+1))
    normalize = normalize_img(fft_mag_log)
    return image_to_base64(normalize)

def normalize_img(img):
    """Normalize the pixel values of an image to the range [0, 255]."""
    return cv2.normalize(img, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8U)

def image_to_base64(img):
    image_utf8 =  base64.b64encode(cv2.imencode('.png', img)[1]).decode('utf-8')
    return 'data:image/png;base64,{}'.format(image_utf8)

def fft_magnitude_details(img,radius):
    """Add details to an FFT magnitude image, such as a cuttof frecuency radius and text annotations."""
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    rows,cols,_ = img.shape
    center_y = int(rows/2)
    center_x = int(cols/2)
    center_coordinates = (center_x, center_y)
    
    color = (255, 0, 255)
    thickness = 2
    image = cv2.circle(img, center_coordinates, radius, color, thickness)
    cv2.putText(image, f'cuttof frecuency:{radius}', (center_x-80, center_y-radius-20), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    return image

def encode_images(images):
    """Encode a list of images in base64 format."""
    return [image_to_base64(img) for img in images]


def apply_gaussian_filter(img, cuttof_frecuencies):
    """Applies the specified frequency filter to the input image for each cutoff frequency and returns the filtered images and spectra."""
    filtered_images = []
    filtered_spectra = []
    for cutoff_frequency in cuttof_frecuencies:
        #Define and apply frequency filter
        filter_params = {"cutoff_frequency": cutoff_frequency,'degree':10}
        filtered_image, filtered_spectrum = apply_low_pass(img, FILTER_TYPE, filter_params)
        #Normalize image in utf8 image format [0,255]
        filtered_image = normalize_img(filtered_image)
        filtered_spectrum = normalize_img(filtered_spectrum)
        #Add some intersting details to frequency plot.
        filtered_spectrum_with_details = fft_magnitude_details(filtered_spectrum,cutoff_frequency)
        filtered_images.append(filtered_image)
        filtered_spectra.append(filtered_spectrum_with_details)
    return filtered_images, filtered_spectra

img  = load_image(IMG_FILE)
# Apply low-pass frequency filter
filter_imgs, filter_spectrums = apply_gaussian_filter(img, CUTOFF_FREQUENCIES)
# Encode filter images in base 64
encoded_imgs = encode_images(filter_imgs)
encoded_filtering = encode_images(filter_spectrums)


# Create Dash application
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = dbc.Container([
    html.H1('Frequency filters'),
    dbc.Row(
        [
            dbc.Col([
                html.H2('Original Image'),
                html.Img(id='image1', src=image_to_base64(img)),
            ], width=2),
            dbc.Col([
                html.H2('Low pass filter image'),
                html.Img(id='filter_image', src=encoded_imgs[0]),
            ], width=2),
            dcc.Interval(
                id='interval-component',
                interval=ANIMATION_INTERVAL, 
                n_intervals=0
            )
        ],
    ),
    dbc.Row(
        [
            dbc.Col([
                html.H2('FFT in the original image'),
                html.Img(id='function', src= full_log_magnitude(img)),
            ], width=2),
            dbc.Col([
                html.H2('FFT low pass filter image'),
                html.Img(id='fft_filter', src=encoded_filtering[0]),
            ], width=2) 
        ])
    ],
    
    )
    

@app.callback(Output('filter_image', 'src'), Output('fft_filter', 'src'), [Input('interval-component', 'n_intervals')])
def update_image(n):
    index = n%len(CUTOFF_FREQUENCIES)
    src_image_1 = encoded_imgs[index]
    src_image_2 = encoded_filtering[index]
    return [src_image_1, src_image_2]

# Run Dash application
if __name__ == '__main__':
    app.run_server(debug=True)