# 🎯 Distance-Based Registration and Attendance System (AI/ML)

This is a real-time AI/ML-powered face recognition application that registers and marks attendance based on the distance between a person’s face and the webcam.

## 🚀 Project Overview

This project combines machine learning, computer vision, and vector databases to create a **smart attendance system** that:

- Detects faces in real time through a webcam
- Calculates the **distance between the face and the webcam**
- Uses that distance to validate presence and trigger registration/attendance
- Stores and retrieves facial embeddings using **Qdrant**, a vector similarity search engine
- Runs the backend using **FastAPI** for API communication

---

## 📦 Features

- 🔍 **Face Recognition**: Detect and recognize faces using embeddings
- 📏 **Distance Estimation**: Custom model to estimate face distance from the webcam
- 🧠 **ML-Driven Attendance**: Register attendance based on face proximity
- 🧰 **Qdrant Integration**: Store and query face embeddings efficiently
- ⚡ **FastAPI Backend**: High-performance API server
- 🎥 Real-time webcam feed processing

---

## 🧠 Technologies Used

| Component       | Stack/Library         |
|-----------------|------------------------|
| Face Detection  | OpenCV, Dlib / FaceNet |
| Distance Model  | Custom ML Model (depth estimation) |
| Backend         | FastAPI (Python)       |
| Vector Database | Qdrant (self-hosted or cloud) |
| Real-Time Feed  | WebSocket, OpenCV      |

---

## 🛠 How It Works

1. **Capture Face from Webcam**  
   The user initiates the camera, and a frame is captured.

2. **Estimate Face Distance**  
   A custom ML model predicts the distance of the face from the webcam.

3. **Generate Face Embedding**  
   A face embedding vector is generated and sent to the backend.

4. **Compare Embedding with Qdrant**  
   The vector is compared with existing entries using cosine similarity or Euclidean distance.

5. **Register / Mark Attendance**  
   If the face matches and is within the valid distance threshold, registration or attendance is marked.

---

## 🚧 Future Work

- Add frontend GUI (PyQt / React)  
- Add Admin Dashboard  
- Add attendance logs and export feature  
- Enhance security and spoof detection  
- Multi-camera / multi-user support

---

## 📸 Sample Flow

```plaintext
[Webcam Input] --> [Face Detection] --> [Distance Model] --> 
[Generate Embedding] --> [Compare with Qdrant DB] --> 
[Register / Mark Attendance]
