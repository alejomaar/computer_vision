import cv2
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import base64
from filter.filter import apply_low_pass
import matplotlib.pyplot as plt
import io

# Load image
img = cv2.imread('img3.png',0)

# Define filter type and filter cuttof ranges
filter_type = "ideal"
cuttof_frecuency_range = list(range(10,100,5))

#Animation rate
refresh_rate = 200


def normalize_uint8(img):
    return cv2.normalize(img, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8U)

def image_to_base64(img):
    image_utf8 =  base64.b64encode(cv2.imencode('.png', img)[1]).decode('utf-8')
    return 'data:image/png;base64,{}'.format(image_utf8)

def encode_images(images):
    return [image_to_base64(img) for img in images]


def apply_gaussian_filter(img, scales):
    filtered_images = []
    filtered_spectra = []
    for cutoff_frequency in scales:
        filtered_image, filtered_spectrum = apply_low_pass(img, filter_type, {"cutoff_frequency": cutoff_frequency})
        filtered_images.append(normalize_uint8(filtered_image))
        filtered_spectra.append(normalize_uint8(filtered_spectrum))

    return filtered_images, filtered_spectra


# Apply low-pass frequency filter
filter_imgs, filter_spectrums = apply_gaussian_filter(img, cuttof_frecuency_range)

# Encode filter images in base 64
encoded_imgs = encode_images(filter_imgs)
encoded_filtering = encode_images(filter_spectrums)


# Crea la aplicación de Dash
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)


#,className="img-fluid"

# Define el layout de la aplicación de Dash
app.layout = dbc.Container([
    html.H1('Frecuency filters'),
    dbc.Row(
        [
            dbc.Col([
                html.H2('Input Image'),
                html.Img(id='image1', src=image_to_base64(img)),
            ], width=2),
            dbc.Col([
                html.H2('Filter image'),
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
                html.H2('FFT Filter'),
                html.Img(id='fft_filter', src=encoded_filtering[0]),
            ], width=2),
            dbc.Col([
                html.H2('Filter function'),
                html.Img(id='function', src= encoded_filtering[-1]),
            ], width=2)
        ])
    ],
    
    )
    

@app.callback(Output('image1', 'src'), Output('fft_filter', 'src'), [Input('interval-component', 'n_intervals')])
def update_image(n):
    index = n%len(cuttof_frecuency_range)
    src_image_1 = encoded_imgs[index]
    src_image_2 = encoded_filtering[index]
    return [src_image_1, src_image_2]

# Ejecuta la aplicación de Dash
if __name__ == '__main__':
    app.run_server(debug=True)