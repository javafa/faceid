from pydantic import BaseModel
from db import crud, db_models
from db.database import SessionLocal
from contextlib import contextmanager

import face_controller
from utils import stringutils

import base64
import io
from PIL import Image

@contextmanager
def session_scope():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

# regist person with face image
class RegistPerson(BaseModel):
    group_id : str
    person_id : str
    person_name : str = None
    img : str # base64 bytes string

def get_persons():
    with session_scope() as db:
        result = crud.get_persons(db)
    return result

def create_person(new_person: RegistPerson) :
    max_img_id = 0
    # db insert person
    result = {}
    print("new_person person==>")
    try :
        with session_scope() as db:
            person_hash = stringutils.generate_person_hash(new_person.group_id, new_person.person_id, new_person.person_name)
            exist_person = crud.get_person(new_person.person_id, db)
            if exist_person is None:
                person = crud.create_person(new_person, person_hash, db)
                print("new_person", person)
            else:
                max_img_id = crud.get_max_img_id(exist_person.person_hash, db)
                person_hash = exist_person.person_hash

            print("new_person max_img_id=", max_img_id)
            print("person_hash", person_hash)

            try: 
                img = Image.open(io.BytesIO(base64.b64decode(new_person.img))).convert("RGB")
            except:
                return {"result":False, "detail":"base64 decoding error"}
            
            result = face_controller.regist_with_align(img, new_person.group_id, person_hash, str(max_img_id))
            print("face regist result", result)
            if result["result"] :
                db_img = crud.create_img(person_hash, max_img_id, db)
    except Exception as e:
        print("new_person exception", e)
        result["result"] = False
        result["description"] = e

    return {"result":result["result"], "detail":result["description"]}

async def add_person(person:RegistPerson):
    print("add person")

