import zmq
import time
import json
import datetime
import matplotlib.pyplot as plt


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


print("Server is awaiting JSON...")

directory = "plots"
while True:
    message = socket.recv_string()
    data = json.loads(message)

    #print(json.dumps(data,indent=4))

    headers = data["data"]["headers"]
    rows = data["data"]["rows"]
    
    if len(headers) != 2:
        socket.send_string("Incorrect number of headers. Please check that the input JSON has 2 headers.")
    elif len(rows[0]) != 2:
        socket.send_string("Incorrect number of columns. Please check that the data has 2 columns.")

    elif data.get("chart_type") == "pie":

        labels = [row[0] for row in rows]
        counts = [row[1] for row in rows]

        #plt.figure()
        plt.pie(counts, labels=labels, autopct= '%1.1f%%')
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fileName = directory+"/pie_chart_"+timestamp+".png"
        plt.savefig(fileName)
        plt.close()
        socket.send_string("Pie Chart Saved")

    elif data.get("chart_type") == "bar":

        labels = [row[0] for row in rows]
        counts = [row[1] for row in rows]

        plt.bar(labels, counts)
        plt.xlabel(headers[0])
        plt.ylabel(headers[1])
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fileName = directory+"/bar_chart_"+timestamp+".png"
        plt.savefig(fileName)
        plt.close()
        socket.send_string("Bar Chart Saved")

    elif data.get("chart_type") == "graph":

        labels = [row[0] for row in rows]
        counts = [row[1] for row in rows]

        plt.plot(labels, counts, marker = 'o')
        plt.xlabel(headers[0])
        plt.ylabel(headers[1])
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fileName = directory+"/line_chart_"+timestamp+".png"
        plt.savefig(fileName)
        plt.close()
        socket.send_string("Line Chart Saved")

    else:
        socket.send_string("Unsupported Chart Type")