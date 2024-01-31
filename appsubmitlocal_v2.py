import base64
import os
from urllib.parse import quote as urlquote

from flask import Flask, send_from_directory
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import boto3
import requests
import pandas as pd

from databaselib import loaderFiletoDB as lf


conn_string = 'postgresql://postgres:imaiden123@localhost:5435/globant_test'

table_columns_dict = {
    'employees': ['id', 'name', 'hire_datetime', 'department_id', 'job_id'],
    'departments': ['id', 'department'],
    'jobs': ['id', 'job_title', 'salary']
}
def read_file_to_df( file_name, table_columns_dict,dic_table_key):
    table_columns = table_columns_dict.get(dic_table_key, [])
    df = pd.read_csv(file_name, header=None, names=table_columns)  # Adjust column names as needed
    if (dic_table_key == 'employees'):
        df['hire_datetime'] = pd.to_datetime(df['hire_datetime'], format = '%Y-%m-%dT%H:%M:%SZ')
        df.drop(columns=['id'],inplace=True)
    return df

UPLOAD_DIRECTORY = "project/app_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)
app = dash.Dash(server=server)


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


app.layout = html.Div(
    [
        html.H1("File Browser"),
        html.H2("Upload"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=True,
        ),
        
        dcc.Loading(
            id="loadingMap",
            type="default",
            children=[ 
                html.H2("File List"),
                html.Ul(id="file-list"),
                html.Ul(id="table-list"),
                dcc.Interval(id='interval-component', interval=1*60*1000, n_intervals=0), 
            ],
        ),  
    ],
    style={"max-width": "500px"},
)


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files



def upload_to_db(file_name, nameTable):
    message =""
    try:
        upload_directory = UPLOAD_DIRECTORY
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
    except FileNotFoundError:
        message = f"File not found {file_name}"
    except pd.errors.EmptyDataError:
        message = f"No data {file_name}"
    except pd.errors.ParserError:
        message = f"Parse error {file_name}"
    except Exception as e:
        message = f"{e} {file_name}"
    else: 
        message = file_name
    finally:
        del(dfTable)  
    
    return(message)

def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


@app.callback(
    Output("file-list", "children"),
    Output("table-list", "children"),
    [Input("upload-data", "filename"), 
     Input("upload-data", "contents"),
     Input('interval-component', 'n_intervals')],
)
def update_output(uploaded_filenames, uploaded_file_contents,n_intervals):
    """Save uploaded files and regenerate the file list."""
    files_over_db = []
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)
            name_table = name.split(".")[0]
            respuesta = upload_to_db( name,  name_table) 
            files_over_db.append(respuesta)
            

    files = uploaded_files()
    if len(files) == 0:
        return [[html.Li("No files yet!")],[html.Li("No files yet!")]]
    else:
        return [[html.Li(file_download_link(filename)) for filename in files],
                [html.Li("Tabla guardada:"+tabla) for tabla in files_over_db]
                ]


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)