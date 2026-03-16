from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.initializers import Orthogonal
from tensorflow.keras.layers import LSTM
import cv2
from functions import download_youtube_videos, predict_single_action
from pytube import YouTube
import os
import numpy as np

app = Flask(__name__)

# Custom LSTM layer to ignore the `time_major` argument
class CustomLSTM(LSTM):
    def __init__(self, *args, **kwargs):
        kwargs.pop('time_major', None)  # Remove the time_major argument if it exists
        super().__init__(*args, **kwargs)

# Load the model with custom objects
custom_objects = {
    'Orthogonal': Orthogonal,
    'LSTM': CustomLSTM}

# Example of loading a model
model = load_model('.\model\LRCN_model__Date_Time_2024_06_23_08_45_06__Loss_0.3223286271095276__Accuracy_0.8770492076873779.h5', custom_objects=custom_objects)

SEQUENCE_LENGTH = 20

@app.route("/members")
def members():
    return {"members": ["member1", "member2"]}

@app.route("/predict", methods=['POST'])
def predict():
    data = request.json
    title = download_youtube_videos(data, './video')
    input_video_file_path = os.path.join('./video', f'{title}')
    print(f'{input_video_file_path}')
    predictionData = predict_single_action(input_video_file_path, SEQUENCE_LENGTH, model)
    return jsonify({'message': f'{title}'}, predictionData)


if __name__ == "__main__":
    app.run(debug=True)