from src.ingest.db import get_engine
from sqlalchemy.orm import sessionmaker

engine = get_engine()

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()