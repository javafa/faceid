from pydantic import BaseModel
from typing import List

# regist person group
class Group(BaseModel):
    group_id: str
    group_name: str = None

# person
class Person(BaseModel):
    person_id: str
    person_name: str = None

# allow role to person
class AllowRole(BaseModel):
    person_id: str
    group_id: str

# regist person with face image
class RegistPerson(BaseModel):
    person_id : str
    person_name : str = None
    img : str # base64 bytes string

# identify face in a group
class IdentifyPerson(BaseModel):
    group_id: str
    img : str # base64 bytes string

# item in results
class IdentifyResultItem(BaseModel):
    distance:int
    person_id:str

# results after identify
class IdentifyResult(BaseModel):
    result: List[IdentifyResultItem] = []