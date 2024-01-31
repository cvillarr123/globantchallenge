# globantchallenge

## Overview

This project provides a simple web application built with Flask and Dash for uploading CSV files, saving them to a local directory, and uploading the data to a PostgreSQL database. The application allows users to browse and download the uploaded files and displays information about the tables created in the database.


## Table of Contents
+ [Project Structure](https://github.com/cvillarr123/globantchallenge/edit/main/README.md## Project Structure)
+ [link](doc:README.md#anchor-links## Project Structure)
+ Setup
+ Usage
+ Dependencies
+ License

## Project Structure

The main components of the project include:

appsubmitlocal_v2.py: The main application file containing the Flask and Dash setup, file upload functionality, and database interactions.
databaselib/loaderFiletoDB.py: Module containing a class (LoadertoDb) for loading data from a Pandas DataFrame to a PostgreSQL database.

reports.py: This application file contains the Flash and Dash setup, report query functionality, and database interactions, using Pandas DataFrame to a PostgreSQL database.
