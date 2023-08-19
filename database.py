from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

#engine = create_engine("postgresql://postgres:8690@localhost/bd-test-carga", echo = True)
engine = create_engine(os.getenv('DATABASE_URL'), echo = True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)