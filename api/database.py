from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
# Absolute path for SQLite database to avoid path issues
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'enrollment.db')}"

print(f"Database path: {SQLALCHEMY_DATABASE_URL}")  # Debug output

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True  # This will show all SQL queries in console for debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        print("Creating new database session...")  # Debug
        yield db
    except Exception as e:
        print(f"Database session error: {e}")  # Debug
        db.rollback()
        raise
    finally:
        print("Closing database session...")  # Debug
        db.close()