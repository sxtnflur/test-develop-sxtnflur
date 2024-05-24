from aiohttp import web
import socketio

ROOM = '1'

sio = socketio.AsyncServer(cors_allowed_origins='*', ping_timeout=35)
app = web.Application()
sio.attach(app)


@sio.event
async def connect(sid, environ):
    print('Connected:', sid)
    # await sio.emit('ready', room=room, skip_sid=sid)

@sio.event
async def join_room(sid, room):
    sio.enter_room(sid, room)

@sio.event
async def left_room(sid, room):
    sio.leave_room(sid, room)

@sio.event
async def disconnect(sid):
    print('Disconnected:', sid)

@sio.event
async def data(sid, data):
    await sio.emit('data', data, skip_sid=sid)


if __name__ == '__main__':
    web.run_app(app, port=9999)
