import dotenv
import os
from pydantic import BaseSettings

class Settings():
    dotenv.load_dotenv()

    app_port = os.getenv("PORT")
    app_host = os.getenv("HOST")
    db_name = os.getenv("POSTGRES_DB")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    DATABASE_URI = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:" \
               f"{db_port}/{db_name}"

settings = Settings()

