from datetime import datetime
from PIL import Image
from src.faceRecognizer import faceRecognizer
from src.utils import *

import base64
import cv2
import io
# import json
import numpy as np
import os
import re
import shutil
import sys
import time
import torch

## Initialize
activate = True

face_database = 'face_database/'
face_temp = 'face_temp/'
mobilefacenet_path = "model_mobilefacenet.pth"
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

faceRecog = faceRecognizer(threshold=0.7, model_path=mobilefacenet_path, 
                                facebank_path=face_database, embedding_size=512, device=device)

## 1. regist group
## input : groupID
# def regist_group(group_id:str):
#     global activate
#     activate = False
#     group_dir = face_database + group_id
#     print("group dir:",group_dir)
#     make_dir(group_dir)
#     activate = True
#     return group_dir

## 2. regist face
## output : result, imgID, description
def regist_with_align(b64_bytes:str, object_id:str, img_id:str):
    result_dict = {}
    global activate
    activate = False

    # handling img data
    try: 
        img = Image.open(io.BytesIO(base64.b64decode(b64_bytes))).convert("RGB")
    except:
        result_dict['result'] = False
        result_dict['description'] = "base64 decoding error"
        activate = True
        return result_dict

    data_dir = face_database + object_id + '/'
    make_dir(data_dir)

    # TODO:agmentation image
    img = align_face(img)
    
    temp_dir = face_temp + object_id + '/'
    make_dir(temp_dir)
    img.save(temp_dir+img_id+".jpg")

    embedding = faceRecog.extract_feature(img)
    embedding = embedding.detach().cpu().numpy()
    
    np.save(data_dir + img_id + ".npy", embedding)
    
    result_dict['result'] = True
    result_dict['description'] = "calculation ok"
    activate = True
    return result_dict



## 3. identify face
## output : result, object_id_list, description
def identify_with_align(b64_bytes:str, group_id:str, threshold:float=2.0, limit=10):
    global activate
    activate = False
    result_dict = {}
    
    # Image Converting
    try:
        b64_image = Image.open(io.BytesIO(base64.b64decode(b64_bytes))).convert("RGB")
    except:
        result_dict['result'] = False
        result_dict['description'] = "base64 decoding error"
        activate = True
        return result_dict

    faceRecog.set_threshold(threshold)
   
    decoded_data = base64.b64decode(b64_bytes)
    np_data = np.fromstring(decoded_data, np.uint8)
    open_cv_image = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)

    img = align_face(b64_image)
    temp_img_name = group_id + "_" + datetime.now().strftime('%Y-%m-%d_%H%M%S') + ".jpg"
    img.save(face_database + temp_img_name)

    result_dict = faceRecog.check_registration(img)
    
    while limit < len(result_dict['object_id_list']):
        del(result_dict['object_id_list'][-1])
    result_dict['count'] = len(result_dict['object_id_list'])
    
    activate = True
    return result_dict