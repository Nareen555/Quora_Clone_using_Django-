from django.db import models
from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, JSON, Numeric,ARRAY,create_engine
    )
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


base = declarative_base()


DATABASE_URL = "postgresql+psycopg2://nareen:Nareen@localhost:5432/project1"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class User(base):
     __tablename__ = "user_details"

     username = Column(String, primary_key = True)
     password = Column(String)
     following = Column(ARRAY(String))




class Posts(base):
     __tablename__="posts"

     request_id = Column(String,primary_key = True)
     username = Column(String)
     post = Column(String)
     vote = Column(JSON)
     created_date = Column(DateTime, default=datetime.utcnow())


class Cmd(base):
     __tablename__="cmd"

     request_id = Column(String,primary_key = True)
     username = Column(String)
     post = Column(String)
     vote = Column(JSON)
     created_date = Column(DateTime, default=datetime.utcnow())
     post_request_id = Column(String)
     




