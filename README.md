# Globantchallenge

## Overview

This project provides a simple web application built with Flask and Dash for uploading CSV files, saving them to a local directory, and uploading the data to a PostgreSQL database. The application allows users to browse and download the uploaded files and displays information about the tables created in the database.

The second Python file is a simple flash/dash web application  to generate two reports that read data from a PostgreSQL generated in the first app.


## Table of Contents for App upload files
+ [Project Structure for Uploading files](https://github.com/cvillarr123/globantchallenge/blob/main/README.md#project-structure)
+ [Setup](https://github.com/cvillarr123/globantchallenge/blob/main/README.md#setup)
+ [Usage](https://github.com/cvillarr123/globantchallenge/blob/main/README.md#usage)
+ [Dependencies](https://github.com/cvillarr123/globantchallenge/blob/main/README.md#dependencies)
+ [License](https://github.com/cvillarr123/globantchallenge/blob/main/README.md#license)

## Project Structure

The main components of the project include:

**appsubmitlocal_v2.py**: The main application file containing the Flask and Dash setup, file upload functionality, and database interactions.
**databaselib/loaderFiletoDB.py**: Module containing a class (LoadertoDb) for loading data from a Pandas DataFrame to a PostgreSQL database.
**reports.py**: This application file contains the Flash and Dash setup, report query functionality, and database interactions, using Pandas DataFrame to a PostgreSQL database.

## Setup

1.  Clone the repository:
git clone https://github.com/your-username/your-repo.git

2.  Install the required dependencies:
pip install -r requirements.txt

3.  Configure the PostgreSQL connection string in the appsubmitlocal_v2.py file:
conn_string = 'postgresql://your_username:your_password@localhost:your_port/your_database'

4.  Configure the PostgreSQL connection string in the reports.py file:
connect_string= 'postgresql://your_username:your_password@localhost:your_port/your_database'

## Run Upload App

4.  Run the application for load :
python appsubmitlocal_v2.py

## Usage for first upload app

1.  Access the application in your web browser at http://localhost:8888.
2.  Use the file upload section to upload CSV files.
3.  The files will be saved to the "project/app_uploaded_files" directory, and information about the tables created in the database will be displayed.
4.  Browse and download the uploaded files.

## Usage for second report app

1.  Access the application in your web browser at http://localhost:8888.
2.  Use a text box to set the year for your query.
3.  Once you set the year, the app shows these two querys:
  a. Number of employees hired for each job and department in a specific year divided by quarter. The table must be ordered alphabetically by department and job.
  b. List of IDs, names and number of employees hired of each department that hired more employees than the mean of employees hired in specific year for all the departments, ordered by the number of employees hired (descending)


## Dependencies

+ Flask
+ Dash
+ Pandas
+ Boto3
+ Requests
+ Psycopg2
+ SqlAlchemy

## License

This project is licensed under the MIT License.
Feel free to customize and use the code as needed!
