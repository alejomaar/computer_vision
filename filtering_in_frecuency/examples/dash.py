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

def normalize_uint8(img):
    return cv2.normalize(img, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8U)


refresh_rate = 200
# Carga la imagen
img = cv2.imread('img3.png',0)
#img =  cv2.resize(img,None, fx = 0.5, fy = 0.5)

# Escalas de filtro gaussiano
scales = list(range(10,100,5))

def apply_gaussian_filter(img, scales):
    filter_type = "ideal"
    def filtering(img,cutoff_frequency):        
        filter_params = {"cutoff_frequency": cutoff_frequency}
        filtered_img, filtered_spectrum = apply_low_pass(img, filter_type, filter_params)
        return normalize_uint8(filtered_img)
    def filtering_spectrum(img,cutoff_frequency):        
        filter_params = {"cutoff_frequency": cutoff_frequency}
        filtered_img, filtered_spectrum = apply_low_pass(img, filter_type, filter_params)
        return normalize_uint8(filtered_spectrum)

    return {'filtered_img': [filtering(img,scale) for scale in scales],
            'filtered_spectrum': [filtering_spectrum(img,scale) for scale in scales] }

def encode_images(images):
    return [base64.b64encode(cv2.imencode('.png', img)[1]).decode('utf-8') for img in images]


# Aplica el filtro gaussiano y crea los objetos de gráfico de plotly
output = apply_gaussian_filter(img, scales)
encoded_imgs = encode_images(output['filtered_img'])
encoded_filtering = encode_images(output['filtered_spectrum'])


# Crea la aplicación de Dash
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)


#,className="img-fluid"

# Define el layout de la aplicación de Dash
app.layout = dbc.Container([
    html.H1('Filtros en frecuencia'),
    dbc.Row(
        [
            dbc.Col([
                html.H2('Input'),
                html.Img(id='image1', src='data:image/png;base64,{}'.format(img)),
            ], width=2),
            dbc.Col([
                html.H2('Filter image'),
                html.Img(id='filter_image', src='data:image/png;base64,{}'.format(encoded_imgs[0])),
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
                html.Img(id='fft_filter', src='data:image/png;base64,{}'.format(encoded_imgs[0])),
            ], width=2),
            dbc.Col([
                html.H2('Filter function'),
                html.Img(id='function', src='data:image/png;base64,{}'.format(encoded_imgs[0])),
            ], width=2)
        ])
    ],
    
    )
    

@app.callback(Output('image1', 'src'), Output('fft_filter', 'src'), [Input('interval-component', 'n_intervals')])
def update_image(n):
    index = n%len(scales)
    src_image_1 = 'data:image/png;base64,{}'.format(encoded_imgs[index])
    src_image_2 = 'data:image/png;base64,{}'.format(encoded_filtering[index])
    return [src_image_1, src_image_2]

# Ejecuta la aplicación de Dash
if __name__ == '__main__':
    app.run_server(debug=True)