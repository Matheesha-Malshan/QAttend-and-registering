'''
import time 
import cv2

cap=cv2.VideoCapture(0)
photos=[]

for i in range(4):
    print(f"Capturing photo {i+1}, please change your face angle slightly...")
    time.sleep(2)  # wait before capture
    ret, frame = cap.read()
    if ret: 
        photos.append(frame)
        cv2.imwrite(f"photo_{i+1}.jpg", frame)

cap.release()
cv2.destroyAllWindows()

'''
from fastapi import FastAPI,WebSocket
from pydantic import BaseModel
import cv2
import numpy as np
import base64
import sys
import os

# Get path to 'a' folder (2 levels up from current file)
import sys
import os



app = FastAPI()

class FrameData(BaseModel):
    image: str

@app.post("/predict")
def process_frame(data: FrameData):
    print(data)

from fastapi import FastAPI, WebSocket

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print("Received:", data)
        await websocket.send_text(f"Prediction for: {data}")