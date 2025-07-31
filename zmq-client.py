import zmq
import time
import json


context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

data = {
    "chart_type": "graph",
    "data": {
        "headers": ["mimetype","count"],
        "rows": [
            ["text/plain", 3],
            ["application/pdf", 7], 
            ["image", 4]
        ]
    }
}

message = json.dumps(data)
socket.send_string(message)

message = socket.recv_string()
print(message)
