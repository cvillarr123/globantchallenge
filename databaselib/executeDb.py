import psycopg2
from psycopg2 import sql, DatabaseError

import psycopg2
import pandas as pd
from sqlalchemy import create_engine


class EmployesDb:
    def __init__(self, conn_string, procedure_name):
        self.conn_string = conn_string
        self.procedure_name = procedure_name
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            # Connect to the PostgreSQL database
            self.conn = psycopg2.connect(self.conn_string)
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise DatabaseError(f"Error connecting to the database: {e}")

    def disconnect(self):
        # Close the cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_merge_procedure(self):
        try:
            # Execute the merge_web_scrapping_data stored procedure
            # the idea is create a sentence as "CALL public.merge_web_scrapping_data();""
            query = "CALL " + self.procedure_name + "();"
            
            self.cursor.execute(query)

            # Commit the changes
            self.conn.commit()

            print("Stored procedure executed successfully!")

        except DatabaseError as e:
            # Handle database-specific exceptions
            error_message = f"DatabaseError: {e}"
            print(error_message)
            raise

        except Exception as e:
            # Handle other exceptions
            error_message = f"Error: {e}"
            print(error_message)
            raise

        finally:
            # Disconnect after execution
            self.disconnect()

# Example usage:
#conn_string = 'postgresql://postgres:imaiden123@localhost:5432/infy_projects'
#merge_processor = MergeWebScrappingData(conn_string)
#merge_processor.connect()
#merge_processor.execute_merge_procedure()

