import cv2
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import base64
from filter.filter import apply_low_pass


refresh_rate = 200
# Carga la imagen
img = cv2.imread('img3.png',0)
img =  cv2.resize(img,None, fx = 0.5, fy = 0.5)

# Escalas de filtro gaussiano
scales = list(range(10,120,2))

def apply_gaussian_filter(img, scales):
    filter_type = "gaussiano"
    def filtering(img,cutoff_frequency):        
        filter_params = {"cutoff_frequency": cutoff_frequency}
        filtered_img, filtered_spectrum = apply_low_pass(img, filter_type, filter_params)
        return filtered_img
    
    return [filtering(img,scale) for scale in scales]

def encode_images(images):
    return [base64.b64encode(cv2.imencode('.png', img)[1]).decode('utf-8') for img in images]

# Aplica el filtro gaussiano y crea los objetos de gráfico de plotly
filtered_imgs = apply_gaussian_filter(img, scales)
encoded_imgs = encode_images(filtered_imgs)


# Crea la aplicación de Dash
app = dash.Dash(__name__)

# Define el layout de la aplicación de Dash
app.layout = html.Div([
    html.Div([
        html.H2('Imagen 1'),
        html.Img(id='image', src='data:image/png;base64,{}'.format(encoded_imgs[0])),
    ], style = {'width': '40%'}),
    dcc.Interval(
        id='interval-component',
        interval=refresh_rate, 
        n_intervals=0
    ),
    html.Div([
        html.H2('Imagen 1'),
        html.Img(id='image2', src='data:image/png;base64,{}'.format(encoded_imgs[0])),
    ], style = {'width': '40%'}),
    html.Div([
        html.H2('Imagen 1'),
        html.Img(id='image3', src='data:image/png;base64,{}'.format(encoded_imgs[0])),
    ], style = {'width': '40%'}),
    html.Div([
        html.H2('Imagen 1'),
        html.Img(id='image4', src='data:image/png;base64,{}'.format(encoded_imgs[0])),
    ], style = {'width': '40%','flex-wrap':'wrap'}),
],style = {'display': 'flex'})

# Define la función de actualización de la imagen
@app.callback(Output('image', 'src'), [Input('interval-component', 'n_intervals')])
def update_image(n):
    index = n%len(scales)
    return 'data:image/png;base64,{}'.format(encoded_imgs[index])


# Ejecuta la aplicación de Dash
if __name__ == '__main__':
    app.run_server(debug=True)