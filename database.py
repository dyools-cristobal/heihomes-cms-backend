from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "mysql+pymysql://root:EmiliaSofia2023!@localhost:3306/HeiHomes"
# URL_DATABASE = "mysql+pymysql://id22178054_root:EmiliaSofia2023!@localhost/id22178054_heihomes"


try:
    engine = create_engine(URL_DATABASE)
    connection = engine.connect()
    print("Connection to the database was successful!")
    connection.close()
except Exception as e:
    print(f"An error occurred: {e}")

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()