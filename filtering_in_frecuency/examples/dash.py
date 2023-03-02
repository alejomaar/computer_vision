import cv2
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import base64

refresh_rate = 500
# Carga la imagen
img = cv2.imread('img3.png')

# Escalas de filtro gaussiano
scales = list(range(2,20))

def apply_gaussian_filter(img, scales):
    return [cv2.blur(img, (scale, scale)) for scale in scales]

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
        html.Img(id='image', src='data:image/png;base64,{}'.format(encoded_imgs[0])),
    ], style={'textAlign': 'center'}),
    dcc.Interval(
        id='interval-component',
        interval=refresh_rate, 
        n_intervals=0
    )
])

# Define la función de actualización de la imagen
@app.callback(Output('image', 'src'), [Input('interval-component', 'n_intervals')])
def update_image(n):
    index = n%len(scales)
    return 'data:image/png;base64,{}'.format(encoded_imgs[index])


# Ejecuta la aplicación de Dash
if __name__ == '__main__':
    app.run_server(debug=True)