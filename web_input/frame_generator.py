import cv2
import base64
import asyncio
import websockets
import json

async def send_frames():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        
        cap = cv2.VideoCapture(0) 

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
           
            await websocket.send(jpg_as_text)
            await asyncio.sleep(0.1)  

            response = await websocket.recv()
            fdata = json.loads(response)

            if fdata and 'error' not in fdata:
                print(f"Distance: {fdata['distance']:.2f} cm | x: {int(fdata['x'])} | y: {int(fdata['y'])} | w: {int(fdata['w'])} | h: {int(fdata['h'])}")
                
                cv2.rectangle(frame,
                                  (int(fdata["x"]),int(fdata["y"])),
                                  (int(fdata["x"]) +int(fdata["w"]), int(fdata["y"])+ int(fdata["h"])),
                                  (255, 0, 0), 2)
                cv2.putText(frame, f"Distance: {fdata['distance']:.2f} cm",
                                (int(fdata["x"]),int(fdata["y"])- 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                (0, 255, 0), 2)
                cv2.imshow('frame',frame)

            else:
                print("[INFO] No face detected.")

          
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

asyncio.run(send_frames())