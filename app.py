from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
counter = 0

@app.route('/')
def serve_static_index():
    return send_from_directory('public', 'index.html')

def send_counter():
    global counter
    while True:
        time.sleep(1)
        socketio.emit('counter', {'value': counter})
        counter += 1

@socketio.on('connect')
def test_connect():
    emit('connected', {'data': 'Connected'})
    threading.Thread(target=send_counter).start()

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
