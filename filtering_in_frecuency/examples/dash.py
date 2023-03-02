import cv2
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import base64

# Carga las dos imágenes
img1 = cv2.imread('img1.png')
img2 = cv2.imread('img2.png')

# Codifica las imágenes en base64 para mostrarlas en Dash
img1_base64 = base64.b64encode(cv2.imencode('.png', img1)[1]).decode('utf-8')
img2_base64 = base64.b64encode(cv2.imencode('.png', img2)[1]).decode('utf-8')

# Crea la aplicación de Dash
app = dash.Dash(__name__)

# Define el layout de la aplicación de Dash
app.layout = html.Div([
    html.Div([
        html.Img(id='image', src='data:image/png;base64,{}'.format(img1_base64)),
    ], style={'textAlign': 'center'}),
    dcc.Interval(
        id='interval-component',
        interval=3000, # Actualiza la imagen cada 3 segundos
        n_intervals=0
    )
])

# Define la función de actualización de la imagen
@app.callback(Output('image', 'src'), [Input('interval-component', 'n_intervals')])
def update_image(n):
    if n % 2 == 0:
        return 'data:image/png;base64,{}'.format(img1_base64)
    else:
        return 'data:image/png;base64,{}'.format(img2_base64)

# Ejecuta la aplicación de Dash
if __name__ == '__main__':
    app.run_server(debug=True)