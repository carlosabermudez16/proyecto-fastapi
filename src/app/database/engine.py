from sqlalchemy import create_engine  # crea la conexión con la base de datos

from app.core.config import settings

db_url = settings.DATABASE_URL
connect_args = {"check_same_thread": False}
is_sqlite = db_url.startswith("sqlite")


# crea el motor de conexión con la db - es el puente entre python y la db
engine = create_engine(
    db_url,
    connect_args=connect_args if is_sqlite else {},
)


