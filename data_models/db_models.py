from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Role(Base):
    __tablename__ = "role"
    role_id      = Column(String, primary_key=True, index=True, nullable=False)
    role_name    = Column(String, index=True)

class Person(Base):
    __tablename__ = "person"
    person_id     = Column(String, primary_key=True, index=True, nullable=False)
    person_name   = Column(String, index=True)

class RoleOfPerson(Base):
    __tablename__ = "role_of_person"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    person_id     = Column(String, index=True, nullable=False)
    role_id      = Column(String, nullable=False)

class Img(Base):
    __tablename__ = "img"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    person_id     = Column(String, ForeignKey("person.person_id"), nullable=False)
    img_id        = Column(Integer)
    data_dir      = Column(String)