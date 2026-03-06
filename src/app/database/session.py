from sqlalchemy.orm import (
    declarative_base,  # le dice a sqlalchemy que todas las clases que heredan de ella son tablas
    sessionmaker,  # crear sesión para conectarse y hablar con la base de datos
)

from app.database.engine import engine

# sqlalchemy necesita saber que clase representan tablas y que clases no,
# por tanto, las clases heredadas de esta base son tablas
base = declarative_base()

# se crea el objeto sesion para interactuar con la base de datos
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    db = session()
    try:
        yield db
    finally:
        db.close()
