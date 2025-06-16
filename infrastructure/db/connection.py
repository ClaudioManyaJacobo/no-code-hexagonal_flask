import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from infrastructure.db.base import Base  

# Cargar variables de entorno
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

user = os.getenv("DB_USER")
password = quote_plus(os.getenv("DB_PASSWORD", ""))
server = os.getenv("DB_SERVER", "localhost")
database = os.getenv("DB_NAME")

if not all([user, password, server, database]):
    raise EnvironmentError("❌ Faltan variables necesarias en el archivo .env")

URL = f"mssql+pytds://{user}:{password}@{server}/{database}"
print(f"🔗 URL de conexión: mssql+pytds://{user}:***@{server}/{database}")

engine = create_engine(URL)
Session = sessionmaker(bind=engine)
