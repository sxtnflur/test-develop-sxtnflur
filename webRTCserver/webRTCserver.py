from flask import Flask, render_template, url_for
import socketio
import eventlet
import eventlet.wsgi
import datetime
from flask_cors import CORS

sio = socketio.Server()
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
cors = CORS(app, origins=['*'], methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'])

connected_particpants = {}

def write_log(s):    
    with open('webrtc/webRTCserver/logfile.txt', 'a+') as f:
        f.write('time: %s Action: %s \n' % (str(datetime.datetime.now()), s))

@app.route('/')
def index():
    """Serve index page"""
    return render_template('index.html', room='default')

@sio.on('message', namespace='/')
def messgage(sid, data):
    sio.emit('message', data=data)

@sio.on('disconnect', namespace='/')
def disconnect(sid):
    # write_log("Received Disconnect message from %s" % sid)
    for room, clients in connected_particpants.items():
        try:
            clients.remove(sid)
            # write_log("Removed %s from %s \n list of left participants is %s" %(sid, room, clients))
        except ValueError:
            # write_log("Remove %s from %s \n list of left participants is %s has failed" %(sid, room, clients))
            pass
@sio.on('create_or_join', namespace='/')
def create_or_join(sid, data):
    # sio.emit('created', data)
    print('create or join')
    print(sid)
    print(data)
    room = data.get('room')
    user_id = data.get('user_id')
    print(room)
    print(user_id)
    sio.enter_room(sid, room)
    print(connected_particpants)

    try:
        connected_particpants[room].append(sid)
    except KeyError:
        connected_particpants[room] = [sid]

    numClients = len(connected_particpants[room])

    if numClients == 1:
        sio.emit('created', room)
    elif numClients > 2:
        sio.emit('full')
    else:
        sio.emit('joined')
        sio.emit('join')
    print(sid, room, len(connected_particpants[room]))

@app.route('/<room>/<user_id>')
def room(room, user_id):
    return render_template('index.html', room=room, user_id=user_id)

if __name__ == '__main__':
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
