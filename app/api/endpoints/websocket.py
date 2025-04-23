
from fastapi import APIRouter,WebSocket,WebSocketDisconnect
import json
import cv2
import numpy as np
import base64
from app.models.dis import Distance_model
from app.models.face_detection import FaceDetector


dm=Distance_model()
router=APIRouter()
fd=FaceDetector()
var=True

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
           
            image_bytes = base64.b64decode(data)
            img_array = np.frombuffer(image_bytes, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
            closest_list=fd.read_and_detect(img)
            
            if closest_list.get("status") == "stop":
                await websocket.send_text(json.dumps(closest_list))
                break 

            
            await websocket.send_text(json.dumps(closest_list)) 

    except WebSocketDisconnect:

        print("Client disconnected gracefully")

