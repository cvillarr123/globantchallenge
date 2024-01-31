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
import pandas as pd


import os

from databaselib import loaderFiletoDB as lf


def save_file(contents, filename):
    # Specify the local directory where you want to save the files
    upload_directory = 'uploads'
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)
    
    filepath = os.path.join(upload_directory, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(contents.replace('\r\n', '\n'))




def read_file_to_df( file_name, table_columns_dict,dic_table_key):
    table_columns = table_columns_dict.get(dic_table_key, [])
    df = pd.read_csv(file_name, header=None, names=table_columns)  # Adjust column names as needed
    if (dic_table_key == 'employees'):
        df['hire_datetime'] = pd.to_datetime(df['hire_datetime'], format = '%Y-%m-%dT%H:%M:%SZ')
        df.drop(columns=['id'],inplace=True)
    return df


def upload_to_db(file_name, nameTable):
    
    upload_directory = 'uploads'
    filepath = os.path.join(upload_directory, file_name)

    dfTable = read_file_to_df(filepath,table_columns_dict,nameTable)
        
    print(dfTable.head(3))
    print('imprime df:')
    print(dfTable.head(2))
    

    loader = lf.LoadertoDb(conn_string,nameTable)
    
    print("entra a dataFrametoTable")
    if (nameTable =='employees'):
        loader = loader.dataFrametoTable(dfTable,'append')
    else:
        loader = loader.dataFrametoTable(dfTable,'replace')
   

    print("sale de dataFrametoTable")
    
    return("File loaded")
# Dash app setup
app = dash.Dash(__name__)
app.title = 'Aplicacion para subir datos:'



# Dictionary to store table names and columns
table_columns_dict = {
    'employees': ['id', 'name', 'hire_datetime', 'department_id', 'job_id'],
    'departments': ['id', 'department'],
    'jobs': ['id', 'job_title', 'salary']
}

# Example: Accessing columns for the 'employees' table
employees_columns = table_columns_dict.get('employees', [])


# Layout of the Dash app
app.layout = html.Div([
    html.H1("S3 File Upload App"),
    html.P("Nombre Archivo:"),
    dcc.Input(id="nameFile", type="text", placeholder="", style={'marginRight':'10px'}),
    html.P("Nombre Tabla:"),
    dcc.Input(id="nameTable", type="text", placeholder="", style={'marginRight':'10px'}),
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

conn_string = 'postgresql://postgres:imaiden123@localhost:5432/infy_projects'

#conn_string = 'postgresql://postgres:imaiden123@localhost:5435/globant_test'




# Dash callback to handle file uploads
@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    Input('nameFile', 'value'),
    Input('nameTable', 'value'),
    prevent_initial_call=True
)
def update_output(contents,filename,nombreTabla):
    if not contents:
        raise PreventUpdate

    content_type, content_string = contents.split(',')
    
    decrypted = base64.b64decode(content_string).decode('utf-8').replace('\r\n', '\n')

    with open('prueba.csv', 'w', encoding='utf-8') as f:
        f.write(decrypted.replace('\r\n', '\n'))
        
    print (decrypted)

    save_file(decrypted, filename)
        
    # Check the response
    
    # Upload each file to S3
    respuesta = upload_to_db( filename,  nombreTabla) 
   
    return html.Div([
        html.H5("Response:"),
        html.Ul(html.Li(respuesta) ),
    ])


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)




#df = pd.read_csv('hired_employees.csv', header=None, names=table_columns_dict.get('employees', [])) 