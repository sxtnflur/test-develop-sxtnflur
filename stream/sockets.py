import base64
import os
import cv2
import numpy as np
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
# from PSN_bot.backend.app import app

from utils import send_error_msg

app = Flask(__name__, static_folder = "./templates/static")

app.config["SECRET_KEY"] = "secret!"
cors = CORS(app, origins=['*'], methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'])
socketio = SocketIO(app, cors_allowed_origins='*')
# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

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
    send_error_msg('image:')
    send_error_msg(image)
    image = base64_to_image(image)
    send_error_msg(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    send_error_msg(gray)
    frame_resized = cv2.resize(gray, (640, 360))
    send_error_msg(frame_resized)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    send_error_msg(encode_param)
    result, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)
    send_error_msg(result)
    send_error_msg(frame_encoded)
    processed_img_data = base64.b64encode(frame_encoded).decode()
    send_error_msg(processed_img_data)
    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + processed_img_data
    send_error_msg(processed_img_data)
    emit("processed_image", processed_img_data)

@app.route("/")
def index():
   return render_template("index.html")

# @app.route("/receive")
# def receive():
#    return render_template("receive.html")

if __name__ == "__main__":
   socketio.run(app, debug = True, port = 5000, host = '0.0.0.0')
