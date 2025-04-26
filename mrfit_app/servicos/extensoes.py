# mrfit_app/extensoes.py

from mrfit_app.config import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
