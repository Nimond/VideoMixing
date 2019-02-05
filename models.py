import datetime
from functools import partial
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
Base = declarative_base()
engine = create_engine('sqlite:///okey.db', echo=True, connect_args={'check_same_thread':False},poolclass=StaticPool)
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    place = Column(String, default='dfghj')
    point = Column(Integer, default=0)
    date = Column(String, default="")
    url = Column(String, default="")
    start_time = Column(String, default="")
    end_time = Column(String, default="")


    def __init__(self,place,point,date,start_time,end_time,url):
        self.place = place
        self.point = point
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.url = url
        
    def __repr__(self):
        return "<User('%i','%i,'%i','%s',)>" % (self.place,self.point,self.date,self.start_time,self.end_time,self.url)


class Place(Base):
    __tablename__ = 'Place'
    id = Column(Integer, primary_key=True)
    place = Column(String, default='dfghj')
    point = Column(Integer, default=0)


    def __init__(self,place,point):
        self.place = place
        self.point = point
        
    def __repr__(self):
        return "<User('%i','%i,'%i','%i','%i','%i','%i','%i','%i','%i','%i','%r','%s',)>" % (self.uid,self.timezone, self.points, self.bot_activated, self.role,self.partner_id, self.points_mor,self.points_eve, self.points_act,self.points_email,self.start_date,self.email)
