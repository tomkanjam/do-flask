from flask import Flask, send_from_directory
import threading
import time
import asyncio
import websockets
import json

app = Flask(__name__)
counter = 0

@app.route('/')
def serve_static_index():
    return send_from_directory('public', 'index.html')

async def send_counter(websocket, path):
    global counter
    while True:
        await asyncio.sleep(1)
        await websocket.send(json.dumps({'counter': counter}))
        counter += 1

def run_websocket_server():
    start_server = websockets.serve(send_counter, "0.0.0.0", 8080)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    threading.Thread(target=run_websocket_server).start()
    app.run(host='0.0.0.0', port=8081)
