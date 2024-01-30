from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# connection string to connect to a database
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/fastapi'#hardcoded version

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

#engine connects sqlalchemy to postgres
engine =create_engine(SQLALCHEMY_DATABASE_URL)

# we need a session to connect/talk to a database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# since a connection can fail hence we use exceptions
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ",error)
#         time.sleep(2)
