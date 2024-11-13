import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import time

# Charger les variables d'environnement
load_dotenv()

# Informations de connexion à la base de données
DB_HOST = os.getenv('DWH_HOST')
DB_PORT = os.getenv('DWH_PORT')
DB_NAME = os.getenv('DWH_DB')
DB_USER = os.getenv('DWH_USER')
DB_PASSWORD = os.getenv('DWH_PASSWORD')

# Fonction pour attendre que PostgreSQL soit prêt
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
            conn_test.close()
            print(f"{host}:5432 - acceptant les connexions")
            return True
        except Exception as e:
            print(f"Erreur de connexion à PostgreSQL : {e}. Nouvelle tentative dans 5 secondes... (Tentative {attempt+1}/5)")
        
        time.sleep(5)
    print("PostgreSQL n'est pas disponible après plusieurs tentatives.")
    return False

if not wait_for_postgres(DB_HOST):
    print("Erreur: PostgreSQL n'est pas disponible après plusieurs tentatives.")
    exit(1)

print("Début du chargement...")

# Connexion à la base de données
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

# Fonction pour mapper les types de données pandas à SQL
def get_sql_type(df_col):
    if pd.api.types.is_integer_dtype(df_col):
        return 'INTEGER'
    elif pd.api.types.is_float_dtype(df_col):
        return 'REAL'
    elif pd.api.types.is_bool_dtype(df_col):
        return 'BOOLEAN'
    else:
        return 'TEXT'

# Chemin des fichiers CSV
data_path = '/opt/Projet_Mouha/data'

# Parcourir tous les fichiers CSV dans le dossier
for filename in os.listdir(data_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(data_path, filename)
        table_name = os.path.splitext(filename)[0]
        transformed_table_name = f"{table_name}_transformed"
        
        # Charger les données dans un DataFrame
        df = pd.read_csv(file_path)
        
        # === Création de la table de base ===
        columns = df.columns
        columns_definition = ', '.join([f"{col} {get_sql_type(df[col])}" for col in columns])
        
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition});"
        cursor.execute(create_table_query)
        conn.commit()
        
        for index, row in df.iterrows():
            placeholders = ', '.join(['%s'] * len(row))
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
            cursor.execute(insert_query, tuple(row))
        conn.commit()
        print(f"Table {table_name} (données brutes) créée avec succès")

        # === Transformations ===
        df.fillna({'CustomerID': 0, 'Description': 'Unknown'}, inplace=True)
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
        df['Total'] = df['Quantity'] * df['UnitPrice']
        df = df[df['UnitPrice'] > 0]
        
        # === Création de la table transformée ===
        transformed_columns = df.columns
        transformed_columns_definition = ', '.join([f"{col} {get_sql_type(df[col])}" for col in transformed_columns])
        
        create_transformed_table_query = f"CREATE TABLE IF NOT EXISTS {transformed_table_name} ({transformed_columns_definition});"
        cursor.execute(create_transformed_table_query)
        conn.commit()
        
        for index, row in df.iterrows():
            placeholders = ', '.join(['%s'] * len(row))
            insert_query = f"INSERT INTO {transformed_table_name} VALUES ({placeholders});"
            cursor.execute(insert_query, tuple(row))
        conn.commit()
        
        print(f"Table {transformed_table_name} (données transformées) créée avec succès")

# Fermer la connexion
cursor.close()
conn.close()
