from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#engine = create_engine("postgresql://postgres:8690@localhost/bd-test-carga", echo = True)
engine = create_engine("postgresql://dreamteam:cjsLndVJRCsRpkXuwIzmCQLvOIZoaEJ5@dpg-cjfgd7gcfp5c7398q260-a.oregon-postgres.render.com/appbdpostgresv1_kgvm", echo = True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)