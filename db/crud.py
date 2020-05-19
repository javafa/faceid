from . import db_models
from fastapi import Depends
from sqlalchemy.orm import Session

from rest_src import rest_models
from rest_src import auth, person

from util import stringutil

# user
def get_user_by_user_id(user_id: str, db: Session):
    table = db_models.User
    return db.query(table).filter(table.user_id == user_id).first()

def create_user(user: auth.SignUp, db: Session):
    hashed_user_id = stringutil.generateHashCode(user.user_id + user.user_name + user.passwd)
    new_user = db_models.User(user_id=user.user_id, user_name=user.user_name, passwd=user.passwd, user_hash=hashed_user_id)
    db.add(new_user)
    return new_user

def get_user(user: auth.SignIn, db: Session):
    table = db_models.User
    user = db.query(table).filter(table.user_id == user.user_id).first()
    return user

# role group
def get_role(role_id: str, db: Session):
    table = db_models.Role
    return db.query(table).filter(table.role_id == role_id).first()

def get_roles(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(db_models.Role).offset(skip).limit(limit).all()

def create_role(role: rest_models.Role, db: Session):
    new_role = db_models.Role(role_id=role.role_id, role_name=role.role_name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

# person
def get_person(person_id: str, db: Session):
    table = db_models.Person
    return db.query(table).filter(table.person_id == person_id).first()

def get_persons(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(db_models.Person).offset(skip).limit(limit).all()

def create_person(person: person.RegistPerson, db: Session):
    new_person = db_models.Person(person_id=person.person_id, person_name=person.person_name)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person

# img
def get_max_img_id(person_id: str, db: Session):
    table = db_models.Img
    max_img_id = 0
    max_img = db.query(table).filter(table.person_id == person_id).order_by(table.img_id.desc()).first()
    if not max_img is None : # 
        max_img_id = max_img.img_id + 1
    return max_img_id

def create_img(person_id: str, max_img_id:int, db: Session):
    new_img = db_models.Img(person_id=person_id, img_id=max_img_id)
    db.add(new_img)
    db.commit()
    db.refresh(new_img)
    return new_img

# roles of person
def get_roles_by_person_id(person_id: str, db: Session):
    table = db_models.RoleOfPerson
    return db.query(table).filter(table.person_id == person_id).all()

def allow_role_to_person(allow:rest_models.AllowRole, db: Session):
    new_role = db_models.RoleOfPerson(person_id=allow.person_id, role_id=allow.role_id)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

def delete_role_of_person(person_id: str, role_id: str, db: Session):
    table = db_models.RoleOfPerson
    role = db.query(table).filter(table.person_id == person_id, table.role_id == role_id).first()
    db.delete(role)
    db.commit()
    return role
