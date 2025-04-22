import cv2
from facenet_pytorch import MTCNN
from facenet_pytorch import InceptionResnetV1
import torch
from app.services.input_pipeline import Input_pipe  

make_data= Input_pipe()
face_recognizer = InceptionResnetV1(pretrained='vggface2').eval()

class FaceDetector:
    def __init__(self):

        self.detector = MTCNN(keep_all=True)  

    def read_and_detect(self):
       
        cap=cv2.VideoCapture(0)
        while True:
            ret,frame=cap.read()
            if not ret:
                break

            rgb_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes,_=self.detector.detect(rgb_frame)
            
            if boxes is not None:
                for box in boxes:
                    x1,y1,x2,y2=map(int,box)
                    x1,y1=max(x1,0),max(y1, 0)
                    x2,y2=min(x2, frame.shape[1]), min(y2, frame.shape[0])

                    box_height = y2-y1
                    print(box_height)
                    cv2.rectangle(frame,(x1, y1),(x2, y2),(0,255,0),2)
                    face_img = frame[y1:y2, x1:x2]

                    face_img = cv2.resize(face_img,(160, 160))
                    input_data=make_data.conver_to_tensors(face_img)
                    face_tensor = torch.tensor(input_data)

                    with torch.no_grad():
                        embedding = face_recognizer(face_tensor)
                       # print("Embedding:", embedding.numpy())

            cv2.imshow('f',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()        

nm=FaceDetector()
nm.read_and_detect()