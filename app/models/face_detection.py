import cv2
from facenet_pytorch import MTCNN 


detector=MTCNN(keep_all=True)
cap=cv2.VideoCapture(0)

while True:
    ret,frame=cap.read()

    if not ret:
        break
    r_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    boxes, _=detector.detect(r_frame)

    if boxes is not None:
        for box in boxes:
            x1,y1,x2,y2=map(int,box)
            x1,y1,x2,y2=max(0, x1),max(0, y1),min(frame.shape[1], x2), min(frame.shape[0], y2)
            color = (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break    


cap.release()
cv2.destroyAllWindows()
