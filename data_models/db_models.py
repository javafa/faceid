from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Group(Base):
    __tablename__ = "group"
    group_id      = Column(String, primary_key=True, index=True, nullable=False)
    group_name    = Column(String, index=True)

class Person(Base):
    __tablename__ = "person"
    person_id     = Column(String, primary_key=True, index=True, nullable=False)
    person_name   = Column(String, index=True)

class RolesToPerson(Base):
    __tablename__ = "roles_to_person"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    person_id     = Column(String, ForeignKey("person.person_id"), nullable=False)
    group_id      = Column(String, ForeignKey("group.group_id"), nullable=False)

    person        = relationship("Person", foreign_keys="roles_to_person.person_id")
    group         = relationship("Group",  foreign_keys="roles_to_person.group_id")

class Img(Base):
    __tablename__ = "img"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    person_id     = Column(String, ForeignKey("person.person_id"), nullable=False)
    img_id        = Column(Integer)
    data_dir      = Column(String)