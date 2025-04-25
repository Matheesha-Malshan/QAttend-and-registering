from fastapi import APIRouter
from pydantic import BaseModel
from app.models.face_detection import embedding_list 
import numpy as np
from app.models.dis import Distance_model
import app.api.endpoints.websocket as web
from qdrant_client.models import PointStruct
from app.api.endpoints.health import client
import uuid

ds=Distance_model()

class RequestData(BaseModel):
    name: str

post_handler=APIRouter()

@post_handler.post("/request/")
async def receive(request_data: RequestData):
   
    rn=np.random.randint(0,10,size=(5,))
    embeddings = np.load(r"C:\Users\HP\dis\app\models\embeddings_.npy")
    labels = np.load(r"C:\Users\HP\dis\app\models\labels_.npy")
    
    embedding_array=np.squeeze(np.array(embedding_list),axis=1)
    
    if request_data.name !='no': #{'shape': '(51, 1, 512)'}

        for i in rn:
            random_id = str(uuid.uuid4())
            
            operation_info = client.upsert(
                collection_name="face_db",
                wait=True,
                points=[
                    PointStruct(
                    id=random_id,
                    vector=embedding_array[i],
                    payload={"name":request_data.name})
                ],
                )
        return {"status":"registered"}

    else:
      
        return {"status":"not *****registered"}
    