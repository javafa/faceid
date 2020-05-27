from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from contextlib import contextmanager

# regist person with face image
class NewGroup(BaseModel): # auto create default group after user's email confirmed
    group_name: str # Default Group

class Group(BaseModel): # auto create default group after user's email confirmed
    group_id: str
    group_name: str # Default Group
    owner_hash: str

def create_group(group_name:str, owner_hash:str):
    try :
        print("group creation")
    except Exception as error:
        print("group creation error", error)
    return None


def delete_group(group_id:str, owner_hash:str):
    try :
        print("delete_group")

    except Exception as error:
        print("group creation error", error)
    return {"result": False, "detail": "could not delete this group"}