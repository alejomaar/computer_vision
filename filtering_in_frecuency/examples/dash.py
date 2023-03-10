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

# Load image
IMG_FILE = 'img/city.png'
img = cv2.imread(IMG_FILE, 0)

# Define filter type and filter cuttof ranges
filter_type = BUTTERWORTH_FILTER
cuttof_frecuencies = list(range(10,100,5))

#Animation rate
refresh_rate = 200

def original_fft_magnitude(img):
    fshift = apply_fft(img)
    fft_mag_log = np.log(abs(fshift+1))
    normalize = normalize_uint8(fft_mag_log)
    return image_to_base64(normalize)

def normalize_uint8(img):
    return cv2.normalize(img, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8U)

def image_to_base64(img):
    image_utf8 =  base64.b64encode(cv2.imencode('.png', img)[1]).decode('utf-8')
    return 'data:image/png;base64,{}'.format(image_utf8)

def draw_circle(img,radius):
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
    return [image_to_base64(img) for img in images]


def apply_gaussian_filter(img, cuttof_frecuencies):
    filtered_images = []
    filtered_spectra = []
    for cutoff_frequency in cuttof_frecuencies:
        filter_params = {"cutoff_frequency": cutoff_frequency,'degree':10}
        filtered_image, filtered_spectrum = apply_low_pass(img, filter_type, filter_params)
        filtered_spectrum = normalize_uint8(filtered_spectrum)
        filtered_spectrum = cv2.cvtColor(filtered_spectrum,cv2.COLOR_GRAY2RGB)
        filtered_spectrum = draw_circle(filtered_spectrum,cutoff_frequency)
        filtered_images.append(normalize_uint8(filtered_image))
        filtered_spectra.append(filtered_spectrum)
    return filtered_images, filtered_spectra


# Apply low-pass frequency filter
filter_imgs, filter_spectrums = apply_gaussian_filter(img, cuttof_frecuencies)

# Encode filter images in base 64
encoded_imgs = encode_images(filter_imgs)
encoded_filtering = encode_images(filter_spectrums)


# Create Dash application
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = dbc.Container([
    html.H1('Frecuency filters'),
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
                interval=refresh_rate, 
                n_intervals=0
            )
        ],
    ),
    dbc.Row(
        [
            dbc.Col([
                html.H2('FFT in the original image'),
                html.Img(id='function', src= original_fft_magnitude(img)),
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
    index = n%len(cuttof_frecuencies)
    src_image_1 = encoded_imgs[index]
    src_image_2 = encoded_filtering[index]
    return [src_image_1, src_image_2]

# Run Dash application
if __name__ == '__main__':
    app.run_server(debug=True)