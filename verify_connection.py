import os
import sys
from sqlalchemy import create_engine, text

# Force reload of config to ensure env vars are picked up
import config

print(f"DB_USER: {config.DB_USER}")
print(f"DB_HOST: {config.DB_HOST}")
print(f"DB_NAME: {config.DB_NAME}")
# Mask password
print(f"DB_PASSWORD: {'*' * len(config.DB_PASSWORD) if config.DB_PASSWORD else 'None'}")

print(f"Target URL: {config.DATABASE_URL}")

try:
    engine = create_engine(config.DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Connection successful! SELECT 1 returned:", result.scalar())
except Exception as e:
    print(f"Connection failed: {e}")
    # If generic failure, try to connect without DB to check if server is reachable
    if "Unknown database" in str(e):
        print("Database does not exist. Attempting to create it...")
        try:
            # Construct URL without DB
            root_url = config.DATABASE_URL.rsplit('/', 1)[0]
            root_engine = create_engine(root_url)
            with root_engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME}"))
                print(f"Database '{config.DB_NAME}' created successfully.")
        except Exception as create_e:
            print(f"Failed to create database: {create_e}")
