
import cv2

class Distance_model:
    def __init__(self):
        
        self.pixel_hight=None
        self.known_distance=30
        self.Real_Height=16
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.cap= cv2.VideoCapture(0)
         
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
                
                focal_length=(h*self.Known_Distance)/self.Real_Height
                #print("focal_length is",focal_length)
                break

        self.cap.release()
        cv2.destroyAllWindows()



    def use_model(self):
       
        focal_length=515.625
        

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
        
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                distance=(self.Real_Height*focal_length)/h
                
                cv2.putText(frame, f"Distance: {distance:.2f} cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0),2)
            
                if cv2.waitKey(1) & 0xFF == ord('a'):
                    print("distance is",distance)

            cv2.imshow("Face Detection", frame)
            
        
            if cv2.waitKey(1) & 0xFF == ord('q'):     
                break

        self.cap.release()
        cv2.destroyAllWindows()

ds=Distance_model()
print(ds.use_model())