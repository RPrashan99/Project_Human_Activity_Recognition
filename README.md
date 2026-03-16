# Human Activity Recognition (HAR)

This repository contains a **Human Activity Recognition** system that uses a deep learning model to classify actions from video. The project includes a **Flask API** that loads a trained model and a **React frontend** that allows users to submit a YouTube video URL and see the predicted activity.

> 🔎 Note: This repository is structured around a pretrained model (`.h5`) and a Flask service. The React app is a basic UI that calls the Flask API.

---

## ✅ Key Features

- 🧠 **Deep learning inference** using a trained LRCN (CNN + LSTM) model
- 🎥 **Video processing pipeline** that samples frames from videos for prediction
- 🌐 **Flask API** exposing a `/predict` endpoint
- 🧩 **React frontend** to submit video URLs and display results
- 📦 Includes a saved model file under `flask-server/model/`

---

## 📂 Repository Structure

```
Project_ROOT/
├── client/                   # React frontend app
│   ├── public/               # Static assets
│   └── src/                  # React source code
├── flask-server/             # Backend API + model inference
│   ├── model/                # Saved model (.h5)
│   ├── server.py             # Flask API entrypoint
│   └── functions.py          # helper utilities (download + inference)
├── model-traning/            # Notebook for training the model
│   └── HumanActivityRecognition.ipynb
└── readme                   # This file (GitHub README)
```

---

## 🛠️ Setup (Local Development)

### 1) Backend (Flask)

1. Create and activate a Python virtual environment (recommended):

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

2. Install required packages:

```bash
pip install flask tensorflow opencv-python pytube numpy
```

3. Start the API server:

```bash
cd flask-server
python server.py
```

The backend runs at: `http://127.0.0.1:5000`

---

### 2) Frontend (React)

1. Install dependencies:

```bash
cd client
npm install
```

2. Start the React development server:

```bash
npm start
```

The frontend will run at: `http://localhost:3000` and proxy API calls to the Flask backend.

---

## 🔌 API Endpoints

### `GET /members`
A quick health check endpoint.

**Response**
```json
{ "members": ["member1", "member2"] }
```

### `POST /predict`
Predicts the activity in a YouTube video.

**Request Body** (plain JSON string containing the full YouTube URL):

```json
"https://www.youtube.com/watch?v=<VIDEO_ID>"
```

> ⚠️ The backend currently expects the request body to be a raw string (not an object).

**Response Example**

```json
{
  "message": "<Video Title>",
  "label_predicted": "Swing",
  "confidence": "0.912345"
}
```

---

## 🧪 Training / Retraining (Optional)

The model training workflow lives in `model-traning/HumanActivityRecognition.ipynb`. This notebook includes data preprocessing, model training, and exporting a `.h5` model file.

If you retrain the model, place the exported model in:

```
flask-server/model/
```

and update `server.py` to load the correct filename.

---

## 💡 Notes / Tips

- The current inference pipeline samples a fixed number of frames (`SEQUENCE_LENGTH = 20`) from the video.
- The model supports the following classes:
  - `WalkingWithDog`
  - `TaiChi`
  - `Swing`
  - `HorseRace`

---

## 📄 License

This project is provided as-is. Add a `LICENSE` file if you want to declare a license.
