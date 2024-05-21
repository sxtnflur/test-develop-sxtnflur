import base64
import os
import random

import cv2
import numpy as np
from flask import Flask, render_template, send_from_directory, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from flask_cors import CORS
from flask import session

app = Flask(__name__, static_folder = "./templates/static")

app.config["SECRET_KEY"] = "secret!"
cors = CORS(app, origins=['*'], methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'])
socketio = SocketIO(app, cors_allowed_origins='*')


is_room = False

def base64_to_image(base64_string):
    base64_data = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_data)
    image_array = np.frombuffer(image_bytes, dtype = np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

@socketio.on("connect")
def connect():
    print("Connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Disconnected")
    # emit("my response", {
    #    "data": "Connected"
    # })

@socketio.on("image")
def receive_image(image):
    # print("IMAGE")
    # print(image)
    image = base64_to_image(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    frame_resized = cv2.resize(gray, (640, 360))
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)
    processed_img_data = base64.b64encode(frame_encoded).decode()
    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + processed_img_data
    emit("processed_image", processed_img_data, broadcast=True)

@socketio.on('joined')
def joined(data):
    # print("joined")
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = data.get('room')
    is_translator = data.get("is_translator")
    # print(room)
    # print(is_translator)
    # if not is_room:
    #     is_room = True
    # else:
    # if room == 7:
    join_room(room)

    emit('join', {'message': 'test'}, room=room)

@socketio.on('leave')
def leave(data):
    user_id = data.get("user_id")
    room = data.get('room')
    leave_room(room)
    emit('leave', {
        "user_id": user_id
    })


# @app.route("/send")
# def send():
#    return render_template("send.html")
#
#
@app.route("/trans/<int:room>/<int:is_translator>")
def receive(room, is_translator):
   return render_template("index.html", room=room, is_translator=is_translator)


@app.route('/send')
def index():
    user_id = random.randint(1, 10)
    return redirect(f"/trans/{user_id}/1")

if __name__ == "__main__":
   socketio.run(app, debug = True, port = 5000, host = '0.0.0.0')