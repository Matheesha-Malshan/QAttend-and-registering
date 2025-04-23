import cv2
from facenet_pytorch import MTCNN
from facenet_pytorch import InceptionResnetV1
import torch
from app.services.input_pipeline import Input_pipe  
import numpy as np
import json
import websocket

make_data= Input_pipe()
face_recognizer = InceptionResnetV1(pretrained='vggface2').eval()
embeddings = np.load(r"C:\Users\HP\dis\app\models\embeddings_.npy")
labels = np.load(r"C:\Users\HP\dis\app\models\labels_.npy")
dis=[]
embedding_list=[]
class FaceDetector:
    def __init__(self):

        self.detector = MTCNN(keep_all=True)  

    def read_and_detect(self,frame):

        rgb_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes,_=self.detector.detect(rgb_frame)
        
        if boxes is not None:
            shape_=boxes.shape[0]
            big_box=np.ones([shape_,4])
            for count,box in enumerate(boxes):
                x1,y1,x2,y2=map(int,box)
                x1,y1=max(x1,0),max(y1, 0)
                x2,y2=min(x2, frame.shape[1]), min(y2, frame.shape[0])

                h,w=y2-y1,x2-x1
                big_box[count]=[x1,y1,w,h]

            big_ind=np.argmax(big_box[:,2])
            big_value=big_box[big_ind]

            face_img=frame[int(y1):int(y1+big_value[3]),int(x1):int(x1+big_value[2])]

            face_img = cv2.resize(face_img,(160, 160))
            input_data=make_data.conver_to_tensors(face_img)
            face_tensor = torch.tensor(input_data)

            with torch.no_grad():
                embedding = face_recognizer(face_tensor).cpu().numpy().squeeze()
            
            nor_embeddings= (embedding/np.linalg.norm(embedding)).reshape(1,-1)
            embedding_list.append(nor_embeddings)
            
            distances = np.linalg.norm(nor_embeddings-embedding, axis=1)

            min_distance = np.min(distances)
            min_index = np.argmin(distances)

            dis.append(min_index)
            cou=len([i for i in dis if 7 < i])
            
            if (len(dis)>50):

                if cou>15:
                    return {"status":"stop",
                            "message":"registered"}
                else:
                    return {"status":"stop",
                            "message":"un registered"}
                    
            else:
                return {"status":"continue"}
        else:
            return {
                    "status":"no face detected"
                    }
    