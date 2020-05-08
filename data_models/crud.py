from sqlalchemy.orm import Session

from . import db_models, rest_models

def get_group(db: Session, group_id: str):
    return db.query(db_models.Group).filter(db_models.Group.group_id == group_id).first()

def get_groups(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(db_models.Group).offset(skip).limit(limit).all()

def create_group(db: Session, group: rest_models.Group):
    db_group = db_models.Group(group_id=group.group_id, group_name=group.group_name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_person(db: Session, person_id: str):
    return db.query(db_models.Person).filter(db_models.Person.person_id == person_id).first()

def get_persons(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(db_models.Person).offset(skip).limit(limit).all()

def create_person(db: Session, person: rest_models.RegistPerson):
    db_person = db_models.Person(person_id=person.person_id, person_name=person.person_name)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def get_max_img_id(db: Session, person_id: str):
    max_img_id = 0
    max_img = db.query(db_models.Img).filter(db_models.Img.person_id == person_id).order_by(db_models.Img.img_id.desc()).first()
    if not max_img is None : # 
        max_img_id = max_img.img_id + 1
    return max_img_id

def create_img(db: Session, person_id: str, max_img_id:int):
    db_img = db_models.Img(person_id=person_id, img_id=max_img_id)
    db.add(db_img)
    db.commit()
    db.refresh(db_img)
    return db_img

def get_persons_by_group_id(db: Session, group_id=str):
    return db.query(db_models.Person).filter(db_models.Person.group_id == group_id).all()


