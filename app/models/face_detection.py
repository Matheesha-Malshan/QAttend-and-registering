import cv2
from facenet_pytorch import MTCNN
from facenet_pytorch import InceptionResnetV1
import torch
from app.services.input_pipeline import Input_pipe  
import numpy as np
from app.api.endpoints.health import client
from collections import Counter

make_data= Input_pipe()
face_recognizer = InceptionResnetV1(pretrained='vggface2').eval()
#embeddings = np.load(r"C:\Users\HP\dis\app\models\embeddings_.npy")
#labels = np.load(r"C:\Users\HP\dis\app\models\labels_.npy")

embedding_list=[]

class FaceDetector:
    def __init__(self):

        self.detector = MTCNN(keep_all=True)  
        self.dist=[]
        self.name=[]
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
            vector=nor_embeddings.flatten().tolist()
         
            search_result=client.search(
            collection_name="face_db",
            query_vector=vector,  # should match the size of your vectors
            limit=1  # Number of nearest vectors to return
                 )
            if search_result:
                distances = [result.score for result in search_result]
                self.dist.append(distances)

                for result in search_result:
                    name = result.payload.get("name") if result.payload else None
                    self.name.append(name)
               
               
            else:
                distance=None
    
            dis_flattened=[item for sublist in self.dist for item in sublist]
            cou = len([i for i in dis_flattened if 0.5>i])
            name_counts = Counter([name for name in self.name if name is not None])

# Get the most common name
            if name_counts:
                most_common_name, name_freq = name_counts.most_common(1)[0]
            else:
                most_common_name, name_freq = None, 0

            if (len(self.dist)>25):
                self.dist=[]
                if cou>15:
                    return {
                    "status": "continue",
                    "message": f"registered ones-{most_common_name}"
                }

                else:
                    return {"status":"stop",
                            "message":"un registered"}
                    
            else:
                return {"status":"cont"}

        else:
            return {
                    "status":"ca"
                    }
    