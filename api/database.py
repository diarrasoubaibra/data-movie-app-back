from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLACHEMY_DATABASE_URL = "sqlite:///./movies.db"

engine = create_engine(
    SQLACHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# if __name__=="__main__":
#     try:
#         with engine.connect() as conn:
#             print("connexion réussie")
#     except Exception as e:
#         print(f"Erreur lors de la conexion: {e}")