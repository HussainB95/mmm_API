import asyncpg
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

db_url = "postgresql://postgres:Myp0stgre$@localhost:5432/mmm"

engine = create_engine(db_url)

session = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

"""load_dotenv()


DB_CONFIG = {
    "user": os.getenv("postgresql"),
    "password": os.getenv("Myp0stgre$"),
    "database": os.getenv("mmm"),
    "host": os.getenv("localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(**DB_CONFIG)

    async with app.state.pool.acquire() as conn:

        await conn.execute(CREATE TABLE IF NOT EXISTS pages (
                id SERIAL PRIMARY KEY,
                slug TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                thumbnail TEXT,                               
                status TEXT NOT NULL DEFAULT 'draft',        
                meta_title TEXT,
                meta_description TEXT,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
                )
        )
    yield
    await app.state.pool.close()"""
