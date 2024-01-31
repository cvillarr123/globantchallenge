import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from requests_aws4auth import AWS4Auth


import boto3
import requests
from io import BytesIO, StringIO

import base64
import csv
import io



import os

# AWS credentials
aws_access_key_id = 'AKIAVSNV2QODP3KKWKU6'
aws_secret_access_key = "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"
aws_region = 'us-west-2'



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
    html.P("Nombre Archivo:"),
    dcc.Input(id="nameFile", type="text", placeholder="", style={'marginRight':'10px'}),
    html.P("Nombre Tabla:"),
    dcc.Input(id="nombretabla", type="text", placeholder="", style={'marginRight':'10px'}),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select File')
        ]),
        multiple=False
    ),
    
    html.Div(id='output-data-upload'),
])

# Helper function to upload file to S3
def upload_to_s3(file_contents, file_name):
   # AWS authentication
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    aws_auth = AWS4Auth(
        aws_access_key_id,
        aws_secret_access_key,
        aws_region,
        'execute-api',
        session_token=session.get_credentials().token
    )   
   
    
    # Send a PUT request to the API endpoint with the file content
    response = requests.put(API_ENDPOINT+"/"+file_name, data=file_contents, headers={'Content-Type': 'text/csv'}, auth=aws_auth)

    if response.status_code == 200:
        print("File successfully submitted to the API.")
    else:
        print(f"Failed to submit the file. Status code: {response.status_code}, Response text: {response.text}")
    return response.status_code 


# Dash callback to handle file uploads
@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    Input('nameFile', 'value'),
    Input('nombretabla', 'value'),
    prevent_initial_call=True
)
def update_output(list_of_contents,filename,nombretabla):
    if not list_of_contents:
        raise PreventUpdate

    if not filename:
        raise PreventUpdate

    if not nombretabla:
        raise PreventUpdate

    print("*********")
    print(list_of_contents)
    print("longitud de list_of_contents")
    print(len(list_of_contents))
    print("*******")

    uploaded_files = []
    for content in list_of_contents:
        content_type, content_string = content.split(',')
        print("Revisar:")
        print(content_type.split(';')[0].split('/')[0])
        print("****")
        
        # Extracting file extension from content type
        file_extension = content_type.split(';')[0].split('/')[1]

        # Generating a unique file name
        
        file_name = filename
        #file_name = f"uploaded_file_{len(uploaded_files) + 1}.{file_extension}"

        #decoded = content_string.encode('utf-8')
        

        decrypted = base64.b64decode(content_string).decode('utf-8')
        print('decrypted')
        print(decrypted)
        
        uploaded_files.append((file_name, decrypted))
        
    # Check the response
    


    #print("uploaded_files")
    #print(uploaded_files)
    # Upload each file to S3
    s3_urls = [upload_to_s3(decoded, file_name) for file_name, decoded in uploaded_files]
   
    

    return html.Div([
        html.H5("Response:"),
        html.Ul([html.Li(file) for file in s3_urls]),
    ])


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
