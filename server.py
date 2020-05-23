import uvicorn

from fastapi import FastAPI, Path, Query, Body, Form, File, UploadFile, HTTPException, Depends
# to use StaticsFiles > pip install aiofiles
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, Response,JSONResponse
# security
# to use html form or OAuth2PasswordRequestForm > pip install python-multipart
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

# fastapi has pydantic 
from pydantic import BaseModel 

from db import crud, db_models
from db.database import engine
from rest_src import rest_models, auth, user, group, person, role, device
import face_controller
from utils import stringutils

from sqlalchemy.orm import Session
from sqlalchemy import exc

from PIL import Image
import base64
import io

db_models.Base.metadata.create_all(bind=engine)

# Title
app = FastAPI(
    title="FaceID",
    description="This is a lightweight face recognition project by ooo.",
    version="0.1.0 Beta",
)

# origins = ['localhost', 'localhost:8000', 'HTTP://127.0.0.1:8000']
# allow_methods=["DELETE", "GET", "POST", "PUT"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=allow_methods,
#     allow_headers=["*"])

# static resource
app.mount("/service", StaticFiles(directory="web"), name="service")
# validators = {"foo": "if you need define this"}

# Check Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authorize")

@app.get("/api/validate")
def validate_token(token: str = Depends(oauth2_scheme)):
    return {"result":True, "token": token}

##########################################
# no Authentication
##########################################
@app.get("/api/status")
async def check_status():
    return {"status":"running"}

@app.get("/api/available/{user_id}")
async def available_user_id(user_id):
    return auth.available_user_id(user_id)

@app.post("/api/signup")
async def sign_up(signup: auth.SignUp) :
    return auth.regist(signup)

@app.post("/api/signin")
async def sign_in(signin: auth.SignIn) :
    result = auth.signin(signin)
    content = {"result":False, "detail": "fail"}
    headers = {}

    print("result===>", result)
    if not result is None:
        if result["result"] :
            datail = result["detail"]
            headers = {"Authorization": "Bearer "+datail["access_token"].decode('utf-8')}
            content["result"] = True
            content["detail"] = "success"
    
    return JSONResponse(content=content, headers=headers)

# to test swagger authorize
# @app.post("/authorize")
# async def authorize(form_data: OAuth2PasswordRequestForm = Depends()) :
#     signin = auth.SignIn(user_id=form_data.username, passwd=form_data.password)
#     result = auth.signin(signin)
#     print(result)
#     return result

##########################################
# Authentication
##########################################
def check_token(token:str = Depends(oauth2_scheme)):
    user = auth.check_token(token)
    return user

## Group
@app.post("/api/group")
async def new_group(new_group: group.NewGroup, auth: str = Depends(check_token)) :
    try :
        owner_hash = auth.user_hash
        group_id = group.create_group(new_group.group_name, owner_hash)
        if not group_id is None :
            face_controller.create_group(group_id)
            return {"result":True, "detail":"ok"}
    except Exception as error:
        print("error group creation", error)
        return {"result":False, "detail":error}
    
    return {"result":False, "detail":"creation failed"}

@app.get("/api/groups")
def get_groups(auth: str = Depends(check_token)):
    try :
        owner_hash = auth.user_hash
        results = group.list_group(owner_hash)
        return {"result":True, "detail": results}
    except Exception as error:
        print("error group list", error)
    
    return {"result":False, "detail": "can not list my groups"}

@app.delete("/api/group/{group_id}")
def remove_group(group_id:str, auth: str = Depends(check_token)):
    try :
        owner_hash = auth.user_hash
        result = group.delete_group(group_id, owner_hash)
        return result
    except Exception as error:
        print("error group list", error)
    
    return {"result":False, "detail": "can not delete the group"}

## Role
@app.post("/api/role")
async def new_role(role: rest_models.Role) :
    try :
        print("new_role", role)
        result = crud.create_role(role)
    except exc.SQLAlchemyError as error:
        return {"result":False, "detail":error}

    return {"result":True, "detail": result}

@app.get("/api/roles")
def get_roles():
    results = crud.get_roles()
    print("roles=",results)
    return {"result":True, "detail": results}

@app.post("/api/allow_role")
async def allow_roles(allow_role: rest_models.AllowRole) :
    # exist user
    if crud.get_person( allow_role.person_id) is None :
        return {"result":False, "detail": "person not exist!"}
    # exist role
    if crud.get_role( allow_role.role_id) is None :
        return {"result":False, "detail": "role not exist!"}
    # already allowed
    roles = crud.get_roles_by_person_id(allow_role.person_id)
    for role in roles :
        if role.role_id == allow_role.role_id :
            return {"result":False, "detail": "already have the same role!"}

    results = crud.allow_role_to_person(allow_role)
    return {"result":True, "detail": results}

## Person
@app.get("/api/persons")
def get_persons(auth: str = Depends(check_token)):
    results = person.get_persons()
    return {"result":True, "detail": results}

@app.post("/api/person")
async def create_person(new_person: person.RegistPerson) :
    print("server in")
    return person.create_person(new_person)

@app.post("/api/identify")
async def identify_person(person: rest_models.IdentifyPerson) :
    try: 
        img = Image.open(io.BytesIO(base64.b64decode(person.img))).convert("RGB")
    except:
        return {"result":False, "detail":"base64 decoding error"}
    result = face_controller.identify_with_align(img, person.role_id)

    return result

@app.get("/test", status_code=307, response_class=Response)
def api_test_in_browser():
    return RedirectResponse('/service/test_face_server.html')

if __name__ == '__main__' :
    uvicorn.run(app, host="0.0.0.0", port=8000)


