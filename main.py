#%% Packages
from venv import create
import pandas as pd

import pyodbc
import psycopg2
from psycopg2 import errors

from sqlalchemy import URL, create_engine

#%% Functions
def get_status(conn) -> None:
    try:
        if conn.closed == 0:
            return "Connection is open"
        else:
            return "Connection is closed"
        return None
    except:
        "You might have not connected to the database"
        return None
    

def extract() -> None:
    db_configs = {"DRIVER": "{SQL Server}",
                  "SERVER": "PCSNT04\BIRD",
                  "DATABASE": "BIDB",
                  "UID": "ten",
                  "PWD": "password"}
    # mssql_conn_str = f"DRIVER={db_configs['DRIVER']};SERVER={db_configs['SERVER']};DATABASE={db_configs['DATABASE']};UID={db_configs['UID']};PWD={db_configs['PWD']}"
    conn = pyodbc.connect(**db_configs)
    mssql_query = "SELECT * FROM dbo.TIPOLD"
    df = pd.read_sql(mssql_query, conn)
    return df

def transform():
    return "NOT IMPLEMENTED"

def load(df) -> None:
    db_configs = {"host": "localhost",
                    "database": "temp_database",
                    "port": 5433,
                    "username": "tenten",
                    "password": "tenten1234"}
    conn_str = URL.create("postgresql", **db_configs)
    engine = create_engine(conn_str)
    conn = engine.connect()
    df.to_sql('new_table', conn, if_exists='replace', index=False)
    return None
#%% Main
def main() -> None:
    df = extract()
    
    load(df)
    # conn = psycopg2.connect(**db_configs)
    # cursor = conn.cursor()
    # query = """CREATE TABLE IF NOT EXISTS testing (
    #             id SERIAL PRIMARY KEY,
    #             name VARCHAR(255) NOT NULL,
    #             date_created TIMESTAMP NOT NULL)"""
    # cursor.execute(query)
    # conn.commit()
    
    # insert_query = """INSERT INTO testing (name, date_created)
    #                 VALUES (%s, %s)"""
    
    # data = ("John", "2023-05-19 10:00:00")
    
    # try:
    #     # Execute the insert query
    #     cursor.execute(insert_query, data)
    #     print("Data inserted successfully!")

    # except psycopg2.Error as e:
    #     if isinstance(e, errors.UniqueViolation):
    #         print("Data already exists!")
    #     else:
    #         print("Error occurred:", e)
        
    # finally:
    #     # Commit the changes to the database
    #     conn.commit()

    #     # Close the cursor and connection
    #     cursor.close()
    #     conn.close()
    return None

#%% Run
if __name__ == "__main__":
    main()