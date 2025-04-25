import sys
import asyncio
import base64
import json
import cv2
import requests
import websockets

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QImage, QPixmap

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)
    update_distance_signal = pyqtSignal(str)
    show_message_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.uri = "ws://localhost:8000/ws"

    async def send_frames(self):
        async with websockets.connect(self.uri) as websocket:
            cap = cv2.VideoCapture(0)
            while self._run_flag:
                ret, frame = cap.read()
                if not ret:
                    break

                _, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')

                await websocket.send(jpg_as_text)
                await asyncio.sleep(0.1)

                response = await websocket.recv()
                fdata = json.loads(response)

                if fdata and fdata.get("status") == "yet":
                    data = fdata["data"]
                    distance_text = f"Distance: {data['distance']:.2f} cm"
                    self.update_distance_signal.emit(distance_text)

                    cv2.rectangle(frame,
                                  (int(data["x"]), int(data["y"])),
                                  (int(data["x"]) + int(data["w"]), int(data["y"]) + int(data["h"])),
                                  (255, 0, 0), 2)
                    cv2.putText(frame, distance_text,
                                (int(data["x"]), int(data["y"]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                (0, 255, 0), 2)

                elif fdata.get("status") in ["error", "continue"]:
                    self.show_message_signal.emit(fdata["message"])

                elif fdata.get("status") == "stop":
                    self.show_message_signal.emit(fdata["message"])
                    self._run_flag = False
                    break

                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.change_pixmap_signal.emit(qt_image)

            cap.release()

    def run(self):
        asyncio.run(self.send_frames())

    def stop(self):
        self._run_flag = False
        self.wait()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registration and Checking")
        self.setGeometry(100, 100, 1200, 700)
        self.initUI()

        self.thread = None

        # Timer to auto-clear messages
        self.clear_message_timer = QTimer(self)
        self.clear_message_timer.setSingleShot(True)
        self.clear_message_timer.timeout.connect(self.clear_message)

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Video Label
        self.video_label = QLabel()
        self.video_label.setFixedSize(800, 600)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("border: 2px solid darkgreen; background-color: white;")

        # Distance Display
        self.distance_label = QLabel("Distance: -- cm")
        self.distance_label.setAlignment(Qt.AlignCenter)
        self.distance_label.setStyleSheet("font-size: 28px; padding: 5px; color: darkgreen;")

        # Message Label (State)
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("font-size: 28px; color: red; padding: 5px;")

        # Name Input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Name")
        self.name_input.setFixedHeight(40)
        self.name_input.setStyleSheet("border: 2px solid darkgreen; padding: 5px; font-size: 16px;")

        # Submit Name Button
        self.submit_button = QPushButton("Submit Name")
        self.submit_button.setStyleSheet("background-color: #32CD32; color: white; font-size: 16px; padding: 10px;")
        self.submit_button.setFixedHeight(40)
        self.submit_button.clicked.connect(self.submit_name)

        # Start Webcam Button
        self.start_button = QPushButton("Start Webcam")
        self.start_button.setStyleSheet("background-color: #228B22; color: white; font-size: 16px; padding: 10px;")
        self.start_button.setFixedHeight(40)
        self.start_button.clicked.connect(self.start_webcam)

        # Layouts
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.distance_label)
        right_layout.addWidget(self.message_label)
        right_layout.addStretch()
        right_layout.addWidget(self.name_input)
        right_layout.addWidget(self.submit_button)
        right_layout.addWidget(self.start_button)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.video_label, alignment=Qt.AlignCenter)
        main_layout.addLayout(right_layout)

        self.central_widget.setLayout(main_layout)

        # Green Background
        self.central_widget.setStyleSheet("background-color: #d0f0c0;")

    def submit_name(self):
        name = self.name_input.text()
        if name:
            try:
                response = requests.post("http://localhost:8000/request/", json={"name": name})
                status = response.json().get("status", "Unknown status")
                self.message_label.setText(status)
                if status.lower() == "registered":
                    self.message_label.setStyleSheet("font-size: 26px; color: green; padding: 5px;")
                else:
                    self.message_label.setStyleSheet("font-size: 26px; color: red; padding: 5px;")
                self.clear_message_timer.start(3000)  # Clear after 3 seconds
            except Exception as e:
                self.message_label.setText(f"Failed to send name: {e}")
                self.clear_message_timer.start(3000)
        else:
            self.message_label.setText("Please enter a name.")
            self.clear_message_timer.start(3000)

    def start_webcam(self):
        if self.thread is None or not self.thread.isRunning():
            self.thread = VideoThread()
            self.thread.change_pixmap_signal.connect(self.update_image)
            self.thread.update_distance_signal.connect(self.update_distance)
            self.thread.show_message_signal.connect(self.show_message)
            self.thread.start()

    def closeEvent(self, event):
        if self.thread:
            self.thread.stop()
        event.accept()

    def update_image(self, qt_image):
        pix = QPixmap.fromImage(qt_image)
        self.video_label.setPixmap(pix.scaled(800, 600, Qt.KeepAspectRatio))

    def update_distance(self, distance):
        self.distance_label.setText(distance)

    def show_message(self, message):
        self.message_label.setText(message)
        self.clear_message_timer.start(3000)  # Clear after 3 seconds

    def clear_message(self):
        self.message_label.setText("")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
