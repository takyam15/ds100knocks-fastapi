from app.postgres.session import SessionLocal


def get_db():
    with SessionLocal() as db:
        yield db
