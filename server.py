import uvicorn

from fastapi import FastAPI, Path, Query, Body, Form, File, UploadFile, HTTPException, Depends
# to use StaticsFiles > pip install aiofiles
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, Response,JSONResponse
# security
# to use html form or OAuth2PasswordRequestForm > pip install python-multipart
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# fastapi has pydantic 
from pydantic import BaseModel 

from db import crud, db_models
from db.database import engine
from rest_src import rest_models, auth, user, group, person, role, device
import face_controller

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

@app.get("/api/userexist/{user_id}")
async def exist_user_id(user_id):
    result = crud.not_exist_user_id(user_id)
    return {"result":result}

@app.post("/api/signup")
async def sign_up(signup: auth.SignUp) :
    return auth.regist(signup)

@app.post("/api/signin")
async def sign_in(signin: auth.SignIn) :
    result = auth.signin(signin)
    print(result)
    content = {"result":False}
    if not result["access_token"] is None:
        headers = {"Authorization": "Bearer "+result["access_token"].decode('utf-8')}
        content["result"] = True
    
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
    print("check_token", user)

@app.post("/api/role")
async def new_role(role: rest_models.Role) :
    try :
        print("new_role", role)
        result = crud.create_role(role)
    except exc.SQLAlchemyError as error:
        return {"result":False, "detail":"role_id is duplicated"}

    return {"result":True, "detail": result}

@app.get("/api/persons")
def get_persons(auth: str = Depends(check_token)):
    results = person.get_persons()
    return {"result":True, "detail": results}

@app.get("/api/roles")
def get_roles():
    results = crud.get_roles()
    print("roles=",results)
    return {"result":True, "detail": results}

@app.post("/api/person")
async def new_person(person: person.RegistPerson) :
    return person.new_person(person)

@app.post("/api/identify")
async def identify_person(person: rest_models.IdentifyPerson) :
    try: 
        img = Image.open(io.BytesIO(base64.b64decode(person.img))).convert("RGB")
    except:
        return {"result":False, "detail":"base64 decoding error"}
    result = face_controller.identify_with_align(img, person.role_id)

    return result

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

@app.get("/test", status_code=307, response_class=Response)
def api_test_in_browser():
    return RedirectResponse('/service/test_face_server.html')

if __name__ == '__main__' :
    uvicorn.run(app, host="0.0.0.0", port=8000)


