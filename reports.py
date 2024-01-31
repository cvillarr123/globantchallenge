# Import necessary libraries
#from flask import Flask, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from sqlalchemy import create_engine
import dash_bootstrap_components as dbc
import flask
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dash import  dash_table as dt

# ... (Your existing code)

# Create SQLAlchemy engine
connect_string= 'postgresql://postgres:imaiden123@localhost:5435/globant_test'

engine = create_engine(connect_string)
conn = engine.connect()


app_flask = flask.Flask(__name__)

app = dash.Dash(__name__, server=app_flask, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config.suppress_callback_exceptions = True

PAGE_SIZE = 10

columns1=['department','job','quarter1','quarter2','quarter3','quarter4']
columns2=['department_id','department','hired_count']
app.layout = html.Div(
    id="first-div",
    children=[
        html.H1("Consulta por año"),
        dcc.Input(
            id='anio',
            value='2020',
            type='text'
        ),
        html.P("Number of employees hired for each job and department in specific year divided by quarter. The table must be ordered alphabetically by department and job. the input for this is year"),
        dt.DataTable(id='data-table1',
            columns=[{"name": i, "id": i} for i in columns1],         

            style_header={
                    'textAlign': 'center',
                    'backgroundColor': 'rgb(220, 220, 220)',
                    'color': 'black',
                    'fontWeight': 'bold',
                    'font-size': '0.7em',
    
            },
    
            page_current=0,
            page_size=PAGE_SIZE,
            page_action='custom',
                
        ),


        html.P("List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in specific year for all the departments, ordered by the number of employees hired (descending)"),
        dt.DataTable(id='data-table2',
            columns=[{"name": i, "id": i} for i in columns2],      

            style_header={
                    'textAlign': 'center',
                    'backgroundColor': 'rgb(220, 220, 220)',
                    'color': 'black',
                    'fontWeight': 'bold',
                    'font-size': '0.7em',
    
            },
    
            page_current=0,
            page_size=PAGE_SIZE,
            page_action='custom',
                
        ),

    ],
    style={"max-width": "500px"},
)


# First query 
# Number of employees hired for each job and department in 2021 divided by quarter. The
# table must be ordered alphabetically by department and job.
# the input for this is year


@app.callback(
    Output(component_id='data-table1',component_property='data'),
    Input("anio", "value"), 
    Input('data-table1', "page_current"),
    Input('data-table1', "page_size"),    
)
def query1(year,page_current,page_size):
        # Replace with your actual SQL query
        sql_query = f"""
            SELECT
                y.department,
                z.job_title AS job,
                COUNT(CASE WHEN EXTRACT(QUARTER FROM x.hire_datetime) = 1 THEN 1 END) AS quarter1,
                COUNT(CASE WHEN EXTRACT(QUARTER FROM x.hire_datetime) = 2 THEN 1 END) AS quarter2,
                COUNT(CASE WHEN EXTRACT(QUARTER FROM x.hire_datetime) = 3 THEN 1 END) AS quarter3,
                COUNT(CASE WHEN EXTRACT(QUARTER FROM x.hire_datetime) = 4 THEN 1 END) AS quarter4
            FROM
                employees x
            JOIN
                departments y ON x.department_id = y.id
            JOIN
                jobs z ON x.job_id = z.id
            WHERE
                EXTRACT(YEAR FROM x.hire_datetime) = {year}
            GROUP BY
                y.department,
                z.job_title
            ORDER BY
                y.department,
                z.job_title;
        """

        result_df = pd.read_sql(sql_query, engine)
        #result = result_df.to_dict(orient='records')
        
        result_df['index'] = range(1, len(result_df) + 1)
        return result_df.iloc[
            page_current*page_size:(page_current+ 1)*page_size
        ].to_dict('records') 

# Second query endpoint
@app.callback(
    Output(component_id='data-table2',component_property='data'),
    Input("anio", "value"), 
    Input('data-table2', "page_current"),
    Input('data-table2', "page_size"),    
)
def query2(year,page_current,page_size):
        # Replace with your actual SQL query
        sql_query = f"""
               SELECT
                x.department_id department_id,
                y.department department,
                COUNT(*) AS hired_count
            FROM
                employees x, departments y
            WHERE
                EXTRACT(YEAR FROM hire_datetime) = {year}
                and x.department_id  = y.id 
            GROUP BY
                department_id,
                department
            HAVING
                COUNT(*) > (
                    SELECT
                        AVG(employee_count)
                    FROM
                        (
                            SELECT
                                COUNT(*) AS employee_count
                            FROM
                                employees
                            WHERE
                                EXTRACT(YEAR FROM hire_datetime) = {year}
                            GROUP BY
                                department_id
                        ) AS subquery
                )
            ORDER BY
                hired_count DESC;
        """

        result_df = pd.read_sql(sql_query, engine)
        #result = result_df.to_dict(orient='records')
        
        result_df['index'] = range(1, len(result_df) + 1)
        return result_df.iloc[
            page_current*page_size:(page_current+ 1)*page_size
        ].to_dict('records') 

# ... (Your existing code)

# Run the application
if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
    #app.run_server(host='0.0.0.0',port=8093,debug=True)    
