from flask import Flask, request, jsonify, render_template
import mediapipe as mp
import cv2
import numpy as np
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

model = load_model('mp_hand_gesture')
with open('gesture.names', 'r') as f:
    classNames = f.read().split('\n')

def process_with_model(image_file):
    filestr = image_file.read()
    npimg = np.fromstring(filestr, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    height, width, _ = frame.shape
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(framergb)
    className = ''

    if results.multi_hand_landmarks:
        landmarks = []
        for hand_landmarks in results.multi_hand_landmarks:
            for lm in hand_landmarks.landmark:
                lmx = lm.x * width
                lmy = lm.y * height
                landmarks.append([lmx, lmy])

        landmarks = np.array(landmarks).reshape(-1, 21, 2) 

        if landmarks.shape == (1, 21, 2):
            prediction = model.predict(landmarks)
            classID = np.argmax(prediction)
            className = classNames[classID]
        else:
            className = "Error in reshaping landmarks"

    return className or "No gesture detected"

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    image_file = request.files['image']
    if image_file:
        result = process_with_model(image_file)
        return jsonify({'result': result})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
