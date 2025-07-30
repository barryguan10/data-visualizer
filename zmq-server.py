import zmq
import time


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    print(f"Received request: {message.decode()}")

    time.sleep(1)
    socket.send(b"This is a message from CS361")
