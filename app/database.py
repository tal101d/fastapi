from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . config import settings
# import psycopg2
# import time
# from psycopg2.extras import RealDictCursor

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLACHEMY_DATABASEURL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'    

engine = create_engine(SQLACHEMY_DATABASEURL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()


#responsable for creating a session to our DB its the best-practice to do that like that so for each API request we'll use this function to gain access to DB
def get_db():           
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


 # in case we want to manage and database using raw SQL instead of SQLAlchemy
# while True: # The Concpet of the loop is keep trying to connect to our database if we failed last time(due to internet lost or something) cause without the data base our app doesn't worth anything
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',
#                                 password='ykykyk123', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connction was succsesfull!")
#         break

#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
