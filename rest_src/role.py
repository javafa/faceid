from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from db import crud, db_models
from db.database import SessionLocal
from contextlib import contextmanager

import face_controller
from utils import stringutils

import base64
import io
from PIL import Image

class Role(BaseModel):
    group_id: str
    role_id: str
    role_name: str

class AllowRole(BaseModel):
    person_id: str
    role_type: str # role or group
    role_or_group_id: str

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

def get_roles(group_id:str):
    try :
        with session_scope() as db:
            results = crud.get_roles(group_id, db)
            return jsonable_encoder(results)
    except Exception as error:
        print("list role error", error)

    return None

def create_role(new_role:Role):
    try :
        with session_scope() as db:
            print("new_role", new_role)
            result = crud.create_role(new_role.group_id, new_role.role_id, new_role.role_name, db)
            return result
    except Exception as error:
        return str(error)