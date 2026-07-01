from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Try PostgreSQL, fallback to local SQLite for developer convenience
try:
    # Using a short timeout for the connection test so it doesn't hang
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        connect_args=(
            {"connect_timeout": 3} if "postgresql" in settings.DATABASE_URL else {}
        ),
    )
    with engine.connect() as conn:
        pass
except Exception:
    fallback_url = "sqlite:///./ridesphere.db"
    engine = create_engine(fallback_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
