import dash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import boto3
import requests
from io import StringIO


# Dash app setup
app = dash.Dash(__name__)
app.title = 'S3 File Upload App'

# AWS S3 configuration
S3_BUCKET = 'buckettestcvifiles'
S3_REGION = 'us-west-2'
S3_BASE_URL = f'https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/'

# API endpoint
API_ENDPOINT = 'https://kh24ljhp48.execute-api.us-west-2.amazonaws.com/dev/buckettestcvifiles'

# Layout of the Dash app
app.layout = html.Div([
    html.H1("S3 File Upload App"),
    
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        multiple=True
    ),
    
    html.Div(id='output-data-upload'),
])

# Helper function to upload file to S3
def upload_to_s3(file_contents, file_name):
    s3 = boto3.client('s3', region_name=S3_REGION)
    s3.upload_fileobj(StringIO(file_contents), S3_BUCKET, file_name)
    return f'{S3_BASE_URL}{file_name}'

# Dash callback to handle file uploads
@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    prevent_initial_call=True
)
def update_output(list_of_contents):
    if not list_of_contents:
        raise PreventUpdate

    uploaded_files = []
    for content in list_of_contents:
        content_type, content_string = content.split(',')
        decoded = content_string.encode('utf-8')
        file_name = content_type.split(';')[1].split('=')[1]
        uploaded_files.append((file_name, decoded))

    # Upload each file to S3
    s3_urls = [upload_to_s3(decoded, file_name) for file_name, decoded in uploaded_files]

    # Call the API with S3 URLs
    api_response = requests.post(API_ENDPOINT, json={'files': s3_urls})

    return html.Div([
        html.H5("Uploaded Files:"),
        html.Ul([html.Li(file) for file in s3_urls]),
        html.H5("API Response:"),
        html.P(api_response.text),
    ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
