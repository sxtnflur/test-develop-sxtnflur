import base64
import os
import cv2
import numpy as np
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
# from PSN_bot.backend.app import app

app = Flask(__name__, static_folder = "./templates/static")

app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

def base64_to_image(base64_string):
    base64_data = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_data)
    image_array = np.frombuffer(image_bytes, dtype = np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

@socketio.on("connect")
def handle_connect():
    print("Connected")
    emit("my response", {
       "data": "Connected"
    })

@socketio.on("disconnect")
def handle_disconnect():
    print("Disconnected")
    # emit("my response", {
    #    "data": "Connected"
    # })

@socketio.on("image")
def receive_image(image):
    image = base64_to_image(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    frame_resized = cv2.resize(gray, (640, 360))
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)
    processed_img_data = base64.b64encode(frame_encoded).decode()
    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + processed_img_data
    emit("processed_image", processed_img_data)

@app.route("/")
def index():
   return render_template("index.html")

if __name__ == "__main__":
   socketio.run(app, debug = True, port = 5000, host = '0.0.0.0', allow_unsafe_werkzeug=True)
