from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Route to our DB. sqlite:///, this is SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./travel.db"

# Our "Engine". The main object that manages the connection
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False})

# Create "Session Fabric"
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class. For create tables
Base = declarative_base()