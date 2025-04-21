import cv2
from facenet_pytorch import MTCNN

class FaceDetector:
    def __init__(self):

        self.detector = MTCNN(keep_all=True)
        self.cap = cv2.VideoCapture(0)
        self.latest_frame = None
        self.running = True

    def read_and_detect(self):
        ret, frame = self.cap.read()
        if not ret:
            self.running = False
            return None, None

        rgb_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes, _=self.detector.detect(rgb_frame)
        self.latest_frame=rgb_frame

        return frame,boxes

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def get_latest_frame(self):
        return self.latest_frame
