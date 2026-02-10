from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import config

# Global variables (initially None or placeholders)
engine = None
SessionLocal = None

# Base class for models
Base = declarative_base()

def init_db(database_url: str = None):
    """
    Initializes the database connection using the provided URL or the one in config.
    """
    global engine, SessionLocal
    
    url = database_url or config.database_url
    if not url:
        raise ValueError("Database URL not configured. Call 'configure()' first.")

    # Create engine (if not already created or if we want to re-init)
    connect_args = {}
    if url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
        
    engine = create_engine(url, connect_args=connect_args)
    
    # Create SessionLocal class
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

def get_db():
    if SessionLocal is None:
        # Auto-initialize if config has a URL (e.g. from environment in main.py)
        # But for library usage, we expect explicit init.
        if config.database_url:
             init_db()
        else:
             raise RuntimeError("Database not initialized. Call 'configure(db_url=...)' first.")
             
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
