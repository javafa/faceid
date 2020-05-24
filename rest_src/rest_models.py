from pydantic import BaseModel
from typing import List

# Person Group

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


