from pydantic import BaseModel
from db import crud, db_models
from db.database import SessionLocal
from contextlib import contextmanager

import face_controller
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

async def new_person(new_person: RegistPerson) :
    max_img_id = 0
    # db insert person
    with session_scope() as db:
        if crud.get_person(new_person.person_id, db) is None:
            person = crud.create_person(new_person, db)
        else:
            max_img_id = crud.get_max_img_id(new_person.person_id)

        try: 
            img = Image.open(io.BytesIO(base64.b64decode(new_person.img))).convert("RGB")
        except:
            return {"result":False, "detail":"base64 decoding error"}

        result = face_controller.regist_with_align(img, new_person.person_id, str(max_img_id))

        if result["result"] :
            db_img = crud.create_img(new_person.person_id, max_img_id)

    return {"result":result["result"], "detail":result["description"]}