import uvicorn
# to use form data > pip install python-multipart
from fastapi import FastAPI, Path, Query, Body, Form, File, UploadFile, HTTPException, Depends
# to use StaticsFiles > pip install aiofiles
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, Response
# fastapi has pydantic 
from pydantic import BaseModel 

from data_models import crud, rest_models, db_models
from data_models.database import SessionLocal, engine
import face_controller

from sqlalchemy.orm import Session
from sqlalchemy import exc

db_models.Base.metadata.create_all(bind=engine)

# Title
app = FastAPI(
    title="BeFace",
    description="This is a lightweight face recognition project by bepluslab.",
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
def check_status():
    return {"status":"running"}

@app.post("/api/group")
async def new_group(group: rest_models.Group, db: Session = Depends(get_db)) :
    try :
        result = crud.create_group(db, group)
    except exc.IntegrityError as error:
        return {"result":"group_id is duplicated"}

    # check group_id directory existence
    # group_dir = face_controller.regist_group(group.group_id)
    return {"result":result}

@app.get("/api/persons")
def get_persons(db: Session = Depends(get_db)):
    results = crud.get_persons(db)
    return {"result":results}

@app.get("/api/groups")
def get_groups(db: Session = Depends(get_db)):
    results = crud.get_groups(db)
    return {"result":results}

@app.post("/api/person")
async def new_person(new_person: rest_models.RegistPerson, db: Session = Depends(get_db)) :
    max_img_id = 0
    # db insert person
    if crud.get_person(db, new_person.person_id) is None:
        person = crud.create_person(db, new_person)
    else:
        max_img_id = crud.get_max_img_id(db, new_person.person_id)
 
    # db insert face image
    db_img = crud.create_img(db, new_person.person_id, max_img_id)
    result = face_controller.regist_with_align(new_person.img, new_person.person_id, str(max_img_id))

    return {"result":str(result["result"]), "detail":result["description"]}

@app.post("/api/identify")
async def identify_person(person: rest_models.IdentifyPerson, db: Session = Depends(get_db)) :
    result = face_controller.identify_with_align(person.img, person.group_id)
    return result

@app.get("/test", status_code=307, response_class=Response)
def api_test_in_browser():
    return RedirectResponse('/service/test_face_server.html')

if __name__ == '__main__' :
    uvicorn.run(app, host="0.0.0.0", port=8000)


