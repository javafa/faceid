from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from contextlib import contextmanager

import face_controller
from utils import stringutils

import base64
import io
from PIL import Image

# regist person with face image
class RegistPerson(BaseModel):
    group_id : str
    person_id : str
    person_name : str = None
    img : str # base64 bytes string

# identify face in a group
class SnapImage(BaseModel):
    group_id: str
    img : str # base64 bytes string

def get_person_by_hash(person_hash:str):
    
    return ""

def get_persons(group_id:str):
    
    return ""

def create_person(new_person: RegistPerson) :
    max_img_id = 0
    # db insert person
    result = {"result":False, "detail":""}
    print("create_person==>")
    try :

        if exist_person is None:
            print("new_person", person)

        try: 
            img = Image.open(io.BytesIO(base64.b64decode(new_person.img))).convert("RGB")
        except:
            return {"result":False, "detail":"base64 decoding error"}
        
        result = face_controller.regist_with_align(img, new_person.group_id, person_hash, str(max_img_id))
        print("face regist result", result)
        
    except Exception as e:
        print("create_person exception", e)
        result["detail"] = e
    return result

def delete_person(person_hash:str) :
    result = {"result":False, "detail":""}
    print("delete_person==>", person_hash)
    try :
        # TODO : check directory existance
        
        if person_hash is None:
            return {"result":False, "detail":"person not exists"}
        else:
            return {"result":True, "detail":"ok"}
    except Exception as e:
        print("delete_person exception", e)
        result["detail"] = e
    return result

def add_person(person:RegistPerson):
    print("add person")

def identify(snap_img: SnapImage) :
    try: 
        img = Image.open(io.BytesIO(base64.b64decode(snap_img.img))).convert("RGB")
        print("person identify img ok")
        result = face_controller.identify_with_align(img, snap_img.group_id)
        return result
    except Exception as e:
        print("identify error", e)
        return {"result":False, "detail":e}
    
    
    