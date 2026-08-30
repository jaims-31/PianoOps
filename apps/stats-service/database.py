import os
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./stats.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def wait_for_db(retries: int = 10, delay: float = 1.5) -> None:

    last_error: Exception | None = None
    for _ in range(retries):
        try:
            with engine.connect():
                return
        except Exception as exc:  # noqa: BLE001 - retry loop needs to catch any connection error
            last_error = exc
            time.sleep(delay)
    raise RuntimeError(
        f"Impossible de se connecter à la base après {retries} tentatives"
    ) from last_error


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
