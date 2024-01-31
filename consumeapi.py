import requests

import requests
import boto3
from requests_aws4auth import AWS4Auth

# AWS credentials
aws_access_key_id = 'AKIAVSNV2QODP3KKWKU6'
aws_secret_access_key = "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"
aws_region = 'us-west-2'


# API endpoint for jobs.csv
api_endpoint = 'https://kh24ljhp48.execute-api.us-west-2.amazonaws.com/dev/buckettestcvifiles/hired_employees.csv'

# Path to the local file you want to upload
file_path =   "project/app_uploaded_files/hired_employees.csv"

# Read the file content
with open(file_path, 'rb') as file:
    file_content = file.read()

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
response = requests.put(api_endpoint, data=file_content, headers={'Content-Type': 'text/csv'}, auth=aws_auth)

# Check the response
if response.status_code == 200:
    print("File successfully submitted to the API.")
else:
    print(f"Failed to submit the file. Status code: {response.status_code}, Response text: {response.text}")


