from fastapi import APIRouter
from pydantic import BaseModel
from app.models.face_detection import embedding_list 
import numpy as np



class RequestData(BaseModel):
    command: str

post_handler=APIRouter()

@post_handler.post("/request")
async def receive(request_data: RequestData):
    
    em_array=np.array(embedding_list)
    if request_data.command=='yes': #{'shape': '(51, 1, 512)'}
        return {"shape":str(em_array.shape)}

    else:
        return {"e":"er"}