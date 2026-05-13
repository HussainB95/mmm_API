import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:My%40dmin1234@localhost:5432/mmm"

engine = create_engine(db_url)

session = sessionmaker(autocommit = False, autoflush = False, bind = engine)