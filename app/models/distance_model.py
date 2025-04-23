"""
import cv2
import numpy as np

class Distance_model:
    def __init__(self):
        
        self.pixel_hight=None
        self.known_distance=30
        self.Real_Height=16
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.cap=cv2.VideoCapture(0)
         
    def train_model(self):

        pixel_hight=None
        while True:
            ret,frame=self.cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces=self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            cv2.imshow("Face Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                
                focal_length=(h*self.known_distance)/self.Real_Height
                print("focal_length is",focal_length)
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def use_model(self,frame):
   
        focal_length=523.125
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        l_n=len(faces)
        
        matrix=np.zeros([l_n,5])
        #print(matrix)
        for count,(x, y, w, h) in enumerate(faces):
            
            distance=(self.Real_Height*focal_length)/h
        
            matrix[count]=[distance,x,y,w,h]

        if matrix.size>0:
            closest_point=np.argmin(matrix[:,0])
            closest_list=matrix[closest_point]

            return{
            "distance":closest_list[0],
            "x":closest_list[1],
            "y":closest_list[2],
            "w":closest_list[3],
            "h":closest_list[4]
            }
        else:
            return {
                "error":"no face detected"
            }

#dm=Distance_model()
#dm.train_model()
"""
import numpy as np

