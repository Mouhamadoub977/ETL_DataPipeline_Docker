import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import subprocess
import time

# load .env variables
load_dotenv()


# database conn info
DB_HOST = os.getenv('DWH_HOST')
DB_PORT = os.getenv('DWH_PORT')
DB_NAME = os.getenv('DWH_DB')
DB_USER = os.getenv('DWH_USER')
DB_PASSWORD = os.getenv('DWH_PASSWORD')


def wait_for_postgres(host):
    for attempt in range(5):
        try:
            conn_test = psycopg2.connect(
                host=host,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            conn_test.close()  # Close connection if successful
            print(f"{host}:5432 - accepting connections")
            return True
        except Exception as e:
            print(f"Error connecting to Postgres: {e}. Retrying in 5 seconds... (Attempt {attempt+1}/5)")
        
        time.sleep(5)

    print("Postgres n'est pas disponible après plusieurs tentatives.")
    return False

if not wait_for_postgres(DB_HOST):
    print("Erreur: PostgreSQL n'est pas disponible après plusieurs tentatives.")
    exit(1)

print("Starting Loading...")

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = conn.cursor()

# get the SQL type from pandas columns types
def get_sql_type(df_col):
    """map pandas types to SQL types"""
    if pd.api.types.is_integer_dtype(df_col):
        return 'INTEGER'
    elif pd.api.types.is_float_dtype(df_col):
        return 'REAL'
    elif pd.api.types.is_bool_dtype(df_col):
        return 'BOOLEAN'
    else:
        return 'TEXT'

# load csv files
data_path = '../data' # within th container
for filename in os.listdir(data_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(data_path, filename)
        table_name = os.path.splitext(filename)[0]
        
        df = pd.read_csv(file_path)
        
        # you can make any tranformation of your data here as you want before loading them
        
        # setup the table structure
        columns = df.columns
        columns_definition = ', '.join([f"{col} {get_sql_type(df[col])}" for col in columns])
        
        # create table
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition});"
        cursor.execute(create_table_query)
        conn.commit()
        
        for index, row in df.iterrows():
            placeholders = ', '.join(['%s'] * len(row))
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
            cursor.execute(insert_query, tuple(row))
        conn.commit()
    print(f"Table {table_name} crée avec succes")

# close the connexiton
cursor.close()
conn.close()