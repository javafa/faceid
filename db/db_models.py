import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from .database import Base
# User
class User(Base):
    __tablename__   = "user"
    no              = Column(Integer, primary_key=True, autoincrement=True)
    user_id         = Column(String, index=True, nullable=False) # email only
    user_name       = Column(String, index=True, nullable=False)
    passwd          = Column(String, nullable=False) #hash
    email_confirmed = Column(Boolean, default=True, nullable=False)
    created         = Column(DateTime, default=datetime.datetime.utcnow)
    last_modified   = Column(DateTime, default=datetime.datetime.utcnow)

# Person Group
class Group(Base):
    __tablename__ = "group"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    group_id      = Column(String, index=True, nullable=False) # auto creation hash string(user_id + group_name + timestamp)
    group_name    = Column(String, index=True)
    user_id       = Column(String, ForeignKey("user.user_id"), nullable=False, index=True)

# Person
class Person(Base):
    __tablename__ = "person"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    person_hash   = Column(String, unique=True, index=True) #hash(group_id + person_id + person_name + timestamp)
    group_id      = Column(String, ForeignKey("group.group_id"), nullable=False)
    person_id     = Column(String, index=True, nullable=False) # usually email
    person_name   = Column(String, index=True)

class RoleOfPerson(Base):
    __tablename__ = "role_of_person"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    person_id     = Column(String, ForeignKey("person.person_id"), nullable=False)
    role_type     = Column(String, nullable=False, default="role") # role or role_group
    role_id       = Column(String, ForeignKey("role.role_id"), nullable=True)
    role_group_id = Column(String, ForeignKey("role_group.role_group_id"), nullable=True)
# Person Images
class Img(Base):
    __tablename__ = "img"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    person_id     = Column(String, ForeignKey("person.person_id"), nullable=False)
    img_id        = Column(Integer)
    data_dir      = Column(String)
# Role
class Role(Base):
    __tablename__ = "role"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    group_id      = Column(String, ForeignKey("group.group_id"), nullable=False)
    role_id       = Column(String, index=True, nullable=False) # auto creation
    role_name     = Column(String, index=True) # attendence, 301 gate etc.

class RoleGroup(Base):
    __tablename__   = "role_group"
    no              = Column(Integer, primary_key=True, autoincrement=True)
    group_id        = Column(String, ForeignKey("group.group_id"), nullable=False)
    role_group_id   = Column(String, index=True, nullable=False) # auto creation
    role_group_name = Column(String, index=True)

class CommandAfterConfirm(Base):
    __tablename__  = "command_after_confirm"
    no             = Column(Integer, primary_key=True, autoincrement=True)
    role_id        = Column(String, ForeignKey("role.role_id"), nullable=False)
    command_id     = Column(String, index=True, nullable=False) # auto creation
    command_name   = Column(String, index=True)
    url            = Column(String)

# Device - role dependency
class AllowDevice(Base):
    __tablename__   = "allow_device"
    no            = Column(Integer, primary_key=True, autoincrement=True)
    device_id     = Column(String, nullable=False, index=True) # auto creation
    device_name   = Column(String, index=True)
    ip_address    = Column(String, nullable=False) # ip + port or url

