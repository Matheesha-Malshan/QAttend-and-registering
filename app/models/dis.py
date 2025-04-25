
import cv2
import numpy as np
from facenet_pytorch import MTCNN
import torch

class Distance_model:
    def __init__(self):
        
        self.pixel_hight=None
        self.known_distance=30
        self.Real_Height=16
        self.face_detect =MTCNN(keep_all=True)
        self.cap=cv2.VideoCapture(0)

    def train_model(self):

        while True:
            ret,frame=self.cap.read()
            if not ret:
                break
        
            rgb_frame= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces,_=self.face_detect.detect(rgb_frame)

            if faces is not None:
                for box in faces:
                    
                    x1,y1,x2,y2=map(int,box)
                    x1,y1=max(x1,0),max(y1, 0)
                    x2,y2=min(x2, frame.shape[1]), min(y2, frame.shape[0])

                    h,w=y2-y1,x2-x1

                    focal_length=(h*self.known_distance)/self.Real_Height
                
                cv2.rectangle(frame,(x1, y1),(x2,y2),(0,255,0),2)

            cv2.imshow('focal length calculator',frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print(focal_length)
                break

        self.cap.release()
        cv2.destroyAllWindows() 

    def use_model(self,frame):
     
        rgb_frame= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces,_=self.face_detect.detect(rgb_frame)
        
        if faces is not None:
          
            shape=faces.shape[0]
            matrix=np.ones([shape,5])
            
            for count,box in enumerate(faces):
                x1,y1,x2,y2=map(int,box)
                x1,y1=max(x1,0),max(y1, 0)
                x2,y2=min(x2, frame.shape[1]), min(y2, frame.shape[0])
                h,w=y2-y1,x2-x1
                distance=(self.Real_Height*256.875)/h
                matrix[count]=[distance,x1,y1,w,h]
            
            closest_dis_in=np.argmin(matrix[:,0])
            cl_distance=matrix[closest_dis_in]
         

            if cl_distance[0]<20:
                return{

                    "status":"ready",

                    
                    }
            
            else:
                
                return{

                    "status":"yet",

                    "data":{
                    "distance":cl_distance[0],
                    "x":cl_distance[1],
                    "y":cl_distance[2],
                    "w":cl_distance[3],
                    "h":cl_distance[4]
                        }
                }
            
        else:
            return {
                "status":"error",
                "message":"no face fucked"
                }
#t=Distance_model()
#t.train_model()