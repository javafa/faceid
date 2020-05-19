from pydantic import BaseModel
from typing import List

# User info.
class SignUp(BaseModel):
    user_id: str # email
    user_name: str
    passwd: str # hashed
    
class SignIn(BaseModel):
    user_id: str # email
    passwd: str # hashed

# Person Group
class PersonGroup(BaseModel): # auto create default group after user's email confirmed
    person_group_id: str # hash(user_id + timestamp)
    person_group_name: str # Default Group
    user_id: str = None # in cookie

# role
class Role(BaseModel):
    group_id: str
    role_id: str = None # auto creation
    role_name: str

class RoleGroup(BaseModel):
    group_id: str
    role_group_id: str = None # auto creation
    role_group_name: str

class RoleToRoleGroup(BaseModel):
    role_group_id: str
    role_id: str

# person
class Person(BaseModel):
    group_id: str
    person_id: str
    person_name: str = None

class AllowRole(BaseModel):
    person_id: str
    role_type: str # role or group
    role_or_group_id: str

# regist person with face image
class RegistPerson(BaseModel):
    group_id : str
    person_id : str
    person_name : str
    img : str # base64 bytes string

# identify face in a group
class IdentifyPerson(BaseModel):
    group_id: str
    role_id: str
    img : str # base64 bytes string
