﻿# globantchallenge

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Title</title>
</head>
<body>

    <h1>Project Title</h1>

    <h2>Overview</h2>

    <p>This project provides a simple web application built with Flask and Dash for uploading CSV files, saving them to a local directory, and uploading the data to a PostgreSQL database. The application allows users to browse and download the uploaded files and displays information about the tables created in the database.</p>

    <h2>Table of Contents</h2>

    <ul>
        <li><a href="#project-structure">Project Structure</a></li>
        <li><a href="#setup">Setup</a></li>
        <li><a href="#usage">Usage</a></li>
        <li><a href="#dependencies">Dependencies</a></li>
        <li><a href="#license">License</a></li>
    </ul>

    <h2>Project Structure</h2>

    <p>The main components of the project include:</p>

    <ul>
        <li><code>app.py</code>: The main application file containing the Flask and Dash setup, file upload functionality, and database interactions.</li>
        <li><code>databaselib/loaderFiletoDB.py</code>: Module containing a class (<code>LoadertoDb</code>) for loading data from a Pandas DataFrame to a PostgreSQL database.</li>
    </ul>

    <h2>Setup</h2>

    <ol>
        <li>Clone the repository:</li>
        <code>git clone https://github.com/your-username/your-repo.git</code>

        <li>Install the required dependencies:</li>
        <code>pip install -r requirements.txt</code>

        <li>Configure the PostgreSQL connection string in the <code>app.py</code> file:</li>
        <code>conn_string = 'postgresql://your_username:your_password@localhost:your_port/your_database'</code>

        <li>Run the application:</li>
        <code>python app.py</code>
    </ol>

    <h2>Usage</h2>

    <ol>
        <li>Access the application in your web browser at <code>http://localhost:8888</code>.</li>
        <li>Use the file upload section to upload CSV files.</li>
        <li>The files will be saved to the "project/app_uploaded_files" directory, and information about the tables created in the database will be displayed.</li>
        <li>Browse and download the uploaded files.</li>
    </ol>

    <h2>Dependencies</h2>

    <ul>
        <li>Flask</li>
        <li>Dash</li>
        <li>Pandas</li>
        <li>Boto3</li>
        <li>Requests</li>
        <li>Psycopg2</li>
    </ul>

    <p>Install the required dependencies using the following:</p>

    <code>pip install Flask Dash pandas boto3 requests psycopg2</code>

    <h2>License</h2>

    <p>This project is licensed under the <a href="LICENSE">MIT License</a>.</p>

    <p>Feel free to customize and use the code as needed!</p>

</body>
</html>
