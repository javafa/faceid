import uvicorn
# to use form data > pip install python-multipart
from fastapi import FastAPI, Path, Query, Body, Form, File, UploadFile, HTTPException, Depends
# to use StaticsFiles > pip install aiofiles
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, Response
# fastapi has pydantic 
from pydantic import BaseModel 

from db import crud, db_models
from db.database import SessionLocal, engine
from rest_src import rest_models
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
# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
# static resource
app.mount("/service", StaticFiles(directory="web"), name="service")
validators = {"foo": "if you need define this"}

@app.get("/api/status")
async def check_status():
    return {"status":"running"}

@app.get("/api/enable_user_id/{user_id}")
async def exist_user_id(user_id, db: Session = Depends(get_db)):
    result = crud.not_exist_user_id(db, user_id)
    return {"result":result}

@app.post("/api/signup")
async def sign_up(signup: rest_models.SignUp, db: Session = Depends(get_db)) :
    try :
        print("signup", signup)
        result = crud.create_user(db, signup)
    except exc.IntegrityError as error:
        return {"result":False, "detail":"could not sign-up!"}
    return {"result":True, "detail": result}

@app.post("/api/signin")
async def sign_in(user: rest_models.SignIn, db: Session = Depends(get_db)) :
    try :
        print("signin", user)
        result = crud.get_user(db, user)
    except exc.IntegrityError as error:
        return {"result":False, "detail":"could not sign-in!"}
    return {"result":True, "detail": result}



@app.post("/api/role")
async def new_role(role: rest_models.Role, db: Session = Depends(get_db)) :
    try :
        print("new_role", role)
        result = crud.create_role(db, role)
    except exc.IntegrityError as error:
        return {"result":False, "detail":"role_id is duplicated"}

    return {"result":True, "detail": result}

@app.get("/api/persons")
def get_persons(db: Session = Depends(get_db)):
    results = crud.get_persons(db)
    print("persons=",results)
    return {"result":True, "detail": results}

@app.get("/api/roles")
def get_roles(db: Session = Depends(get_db)):
    results = crud.get_roles(db)
    print("roles=",results)
    return {"result":True, "detail": results}

@app.post("/api/person")
async def new_person(new_person: rest_models.RegistPerson, db: Session = Depends(get_db)) :
    max_img_id = 0
    # db insert person
    if crud.get_person(db, new_person.person_id) is None:
        person = crud.create_person(db, new_person)
    else:
        max_img_id = crud.get_max_img_id(db, new_person.person_id)

    try: 
        img = Image.open(io.BytesIO(base64.b64decode(new_person.img))).convert("RGB")
    except:
        return {"result":False, "detail":"base64 decoding error"}

    result = face_controller.regist_with_align(img, new_person.person_id, str(max_img_id))

    if result["result"] :
        db_img = crud.create_img(db, new_person.person_id, max_img_id)

    return {"result":result["result"], "detail":result["description"]}

@app.post("/api/identify")
async def identify_person(person: rest_models.IdentifyPerson, db: Session = Depends(get_db)) :
    try: 
        img = Image.open(io.BytesIO(base64.b64decode(person.img))).convert("RGB")
    except:
        return {"result":False, "detail":"base64 decoding error"}
    result = face_controller.identify_with_align(img, person.role_id)

    return result

@app.post("/api/allow_role")
async def allow_roles(allow_role: rest_models.AllowRole, db: Session = Depends(get_db)) :
    # exist user
    if crud.get_person(db, allow_role.person_id) is None :
        return {"result":False, "detail": "person not exist!"}
    # exist role
    if crud.get_role(db, allow_role.role_id) is None :
        return {"result":False, "detail": "role not exist!"}
    # already allowed
    roles = crud.get_roles_by_person_id(db, allow_role.person_id)
    for role in roles :
        if role.role_id == allow_role.role_id :
            return {"result":False, "detail": "already have the same role!"}

    results = crud.allow_role_to_person(db, allow_role)
    return {"result":True, "detail": results}

@app.get("/test", status_code=307, response_class=Response)
def api_test_in_browser():
    return RedirectResponse('/service/test_face_server.html')

if __name__ == '__main__' :
    uvicorn.run(app, host="0.0.0.0", port=8000)


