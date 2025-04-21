import cv2
import requests
import base64

cap=cv2.VideoCapture(0)

while True:
    ret,frame=cap.read()
    
    if not ret:
       break

    cv2.imshow("Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()    

import asyncio
import websockets

async def send_frames():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        for i in range(5):
            message = f"Frame {i}: hhh malshan"
            await websocket.send(message)
            response = await websocket.recv()
            print("Server response:", response)

asyncio.run(send_frames())

