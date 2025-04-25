
from fastapi import APIRouter,WebSocket,WebSocketDisconnect
import json
import cv2
import numpy as np
import base64
from app.models.dis import Distance_model
from app.models.face_detection import FaceDetector
import asyncio

dm=Distance_model()
router=APIRouter()
fd=FaceDetector()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    counter_v=0
    print("malshan")
    closest_list = {"status": "yet"}
    try:
        
        while True:
            
            data = await websocket.receive_text()

            image_bytes = base64.b64decode(data)
            img_array = np.frombuffer(image_bytes, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            closest_list=dm.use_model(img)

            
            if closest_list.get("status") =="ready":
                closest_list=fd.read_and_detect(img)
                 
                if closest_list.get("status") == "stop":
                    await websocket.send_text(json.dumps(closest_list))
                    break
                if closest_list.get("status") == "continue":
                    
                    await websocket.send_text(json.dumps(closest_list))
                   

                else:
                    await websocket.send_text(json.dumps(closest_list))
            else:
                await websocket.send_text(json.dumps(closest_list))  
            """
            if closest_list.get("status")=="continue":
                closest_list=dm.use_model(img)
                
                await websocket.send_text(json.dumps(closest_list))
         
            if closest_list.get("status") =="yet":
                await websocket.send_text(json.dumps(closest_list))
                 """ 
            

    except WebSocketDisconnect:

        print("Client disconnected gracefully")

