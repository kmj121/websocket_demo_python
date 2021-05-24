import eventlet
import socketio
import requests

# create a Socket.IO Client
sio = socketio.Client()

@sio.event
def connect():
    print("connect established")
    sio.emit("my_event", {"response":"my response"})

@sio.event
def my_message(data):
    print("message received with:", data)

@sio.event
def dis_connect():
    print('disconnected from server')

sio.connect("http://localhost:5000")
sio.wait()
