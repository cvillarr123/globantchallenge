import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from psycopg2 import sql, DatabaseError


class LoadertoDb:
    def __init__(self, conn_string, table_name):
        self.conn_string = conn_string
        self.table_name = table_name

        self.conn = None


    def connect(self):
        try:
            # Connect to the PostgreSQL database
            #self.conn = psycopg2.connect(self.conn_string)
            db = create_engine(self.conn_string)
            self.conn = db.connect()
            print("connect exitoso")
        except Exception as e:
            raise DatabaseError(f"Error connecting to the database: {e}")

    def disconnect(self):
        # Close the cursor and connection
        if self.conn:
            self.conn.close()  
            print("disconnect exitoso")
            
#conn_string = 'postgresql://postgres:imaiden123@localhost:5432/infy_projects'
    def dataFrametoTable(self, df,tipo_carga ):
        # Create DataFrame
        try:
            engine = create_engine(self.conn_string)
            print(self.conn_string)
            print(self.table_name)

            print('dataframe:')
            print(df.head(3))
            print("va a cargar la tabla: ", self.table_name)
            df.to_sql(self.table_name, engine,if_exists=tipo_carga,index=False)


            print("finalizo carga a la  tabla: ", self.table_name)
        except Exception as e:
            raise DatabaseError(f"Error connecting to the database: {e}")
            return("error")
        
        return ("exito")




# load_to_db(dfDataWeb,conn_string,'web_scrapping_gov_tmp')