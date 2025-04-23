import cv2
import base64
import asyncio
import websockets
import json
import requests

durl="ws://localhost:8000/ws"

async def send_frames():
    uri =durl
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

            if fdata and fdata.get("status") == "success":
                data = fdata["data"]
                print(f"Distance: {data['distance']:.2f} cm | x: {int(data['x'])} | y: {int(data['y'])} | w: {int(data['w'])} | h: {int(data['h'])}")
                
                cv2.rectangle(frame,
                            (int(data["x"]), int(data["y"])),
                            (int(data["x"]) + int(data["w"]), int(data["y"]) + int(data["h"])),
                            (255, 0, 0), 2)
                
                cv2.putText(frame, f"Distance: {data['distance']:.2f} cm",
                            (int(data["x"]), int(data["y"]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                            (0, 255, 0), 2)
                
                cv2.imshow('frame',frame)

            elif fdata.get("status") == "error":
                print(f"[INFO] {fdata['message']}")
            
            elif fdata.get("status")=="stop":
                print(f"stop framing{fdata['message']}")
                
                user_input=input("Enter yes or no")
                
                if user_input.lower() == "yes":
                    response = requests.post("http://localhost:8000/request",
                                              json={"command":"yes"})
                    print(response.json())
                elif user_input.lower() =="no":
                    response = requests.post("http://localhost:8000/request",
                                              json={"command":"no"})
                    print(response.json())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

asyncio.run(send_frames())