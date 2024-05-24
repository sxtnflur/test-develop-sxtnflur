from flask import Flask, render_template, request
import eventlet
import socketio
import eventlet.wsgi

sio = socketio.Server()#async_mode=async_mode)
app = Flask(__name__, template_folder='web', static_folder='static')
# app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
ROOM = '1'

@app.route('/viewer')
def viewer():
	return render_template('viewer.html', room=ROOM)

@app.route('/presenter')
def index():
	return render_template('presenter.html', room=ROOM)

if __name__ == '__main__':
	# eventlet.wsgi.server(eventlet.listen(('0.0.0.0',5000)), app)
	app.run('127.0.0.1', 7000)