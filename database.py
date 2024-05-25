from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "mysql+pymysql://root:EmiliaSofia2023!@localhost:3306/HeiHomes"
# URL_DATABASE = "mysql+pymysql://u810413882_heihomes:livewithHEI1989!@srv1387.hstgr.io:3306/u810413882_heihomes"


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