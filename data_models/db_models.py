from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Group(Base):
    __tablename__ = "group"
    group_id = Column(String, primary_key=True, index=True)
    group_name = Column(String, index=True)

class Person(Base):
    __tablename__ = "person"
    person_id = Column(String, primary_key=True, index=True)
    person_name = Column(String, index=True)

class PersonInGroup(Base):
    __tablename__ = "person_in_group"
    no = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(String, ForeignKey("person.person_id"))
    group_id = Column(String, ForeignKey("group.group_id"))

class Img(Base):
    __tablename__ = "img"
    no = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(String, ForeignKey("person.person_id"))
    img_id = Column(Integer)
    data_dir = Column(String)