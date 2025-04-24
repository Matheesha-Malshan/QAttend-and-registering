import sys
import cv2
import asyncio
import base64
import json
import requests
import websockets
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

class CameraThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)
    update_distance = pyqtSignal(str)

    def __init__(self, name_getter):
        super().__init__()
        self.name_getter = name_getter
        self.running = True

    async def send_frames(self):
        uri = "ws://localhost:8000/ws"
        async with websockets.connect(uri) as websocket:
            cap = cv2.VideoCapture(0)

            while self.running:
                ret, frame = cap.read()
                if not ret:
                    continue

                _, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')

                await websocket.send(jpg_as_text)
                await asyncio.sleep(0.1)

                response = await websocket.recv()
                fdata = json.loads(response)

                if fdata and fdata.get("status") == "yet":
                    data = fdata["data"]
                    distance_text = f"Distance: {data['distance']:.2f} cm"
                    self.update_distance.emit(distance_text)

                    cv2.rectangle(frame,
                                  (int(data["x"]), int(data["y"])),
                                  (int(data["x"]) + int(data["w"]), int(data["y"]) + int(data["h"])),
                                  (255, 0, 0), 2)

                    cv2.putText(frame, distance_text,
                                (int(data["x"]), int(data["y"]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                (0, 255, 0), 2)

                elif fdata.get("status") == "stop":
                    name = self.name_getter()
                    if name.lower() == "no":
                        continue
                    requests.post("http://localhost:8000/request/", json={"name": name})
                    websocket = await websockets.connect(uri)

                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.change_pixmap_signal.emit(qt_image)

            cap.release()

    def run(self):
        asyncio.run(self.send_frames())

    def stop(self):
        self.running = False
        self.quit()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome registration and checking")
        self.setGeometry(100, 100, 1000, 600)
        self.setup_ui()

        self.camera_thread = CameraThread(self.get_name_input)
        self.camera_thread.change_pixmap_signal.connect(self.update_image)
        self.camera_thread.update_distance.connect(self.update_distance_box)

    def setup_ui(self):
        layout = QGridLayout()

        self.video_label = QLabel("Camera View")
        self.video_label.setStyleSheet("background-color: #4682B4;")
        self.video_label.setFixedSize(500, 300)

        self.distance_box = QLabel("Distance and message")
        self.distance_box.setStyleSheet("background-color: #4682B4; color: white;")
        self.distance_box.setAlignment(Qt.AlignCenter)
        self.distance_box.setFixedHeight(60)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Type name here")

        self.name_input_2 = QLineEdit()
        self.name_input_2.setPlaceholderText("If not registered enter the name")

        self.register_button = QPushButton("Registering")
        self.check_button = QPushButton("Checking")
        self.webcam_button = QPushButton("On web cam")

        self.webcam_button.clicked.connect(self.start_camera)

        layout.addWidget(QLabel("Welcome registration and checking"), 0, 0, 1, 3, alignment=Qt.AlignCenter)
        layout.addWidget(self.video_label, 1, 0, 3, 2)
        layout.addWidget(self.distance_box, 1, 2)
        layout.addWidget(self.name_input, 2, 2)
        layout.addWidget(self.name_input_2, 3, 2)
        layout.addWidget(self.register_button, 4, 0)
        layout.addWidget(self.check_button, 5, 0)
        layout.addWidget(self.webcam_button, 6, 0, 1, 3)

        self.setLayout(layout)

    def get_name_input(self):
        return self.name_input.text().strip() or self.name_input_2.text().strip()

    def start_camera(self):
        if not self.camera_thread.isRunning():
            self.camera_thread.start()

    def update_image(self, qt_image):
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def update_distance_box(self, text):
        self.distance_box.setText(text)

    def closeEvent(self, event):
        self.camera_thread.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())
