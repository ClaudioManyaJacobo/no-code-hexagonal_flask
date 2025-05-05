# infrastructure/db/connection.py
import pymssql
import os
from dotenv import load_dotenv

# Carga variables de entorno desde .env
load_dotenv()

def get_connection():
    return pymssql.connect(
        server=os.getenv("DB_SERVER"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
