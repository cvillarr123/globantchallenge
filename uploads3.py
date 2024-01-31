import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import os 



import boto3
import requests
from io import StringIO

client = boto3.client('s3')



bucket = 'buckettestcvifiles'
cur_path = os.getcwd()
file = 'hired_employees_copia.csv'

filename = os.path.join(cur_path,'data', file)

#open the file
data = open(filename,'rb')

#load data into S3
client.upload_file(filename,bucket,file)
