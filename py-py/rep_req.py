from tkinter import image_types
from pandas import value_counts
import zmq
import sys
import time

def start_client():
    context = zmq.Context()

    #  Socket to talk to server
    print("Connecting to hello world server…")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    funcs = ['add 1 2', 'mul 2 3', 'exit']
    for idx in range(len(funcs)):
        fun = funcs[idx].encode('utf-8')
        socket.send(fun)
        result = socket.recv().decode('utf-8')
        print(f'{fun} result is {result}')
        if result == 'exit':
            break

def start_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        msg = socket.recv().decode('utf-8')
        items = msg.split(' ')
        cmd_type = items[0]
        if cmd_type == 'add':
            result = int(items[1]) + int(items[2])
        elif cmd_type == 'mul':
            result = int(items[1]) * int(items[2])
        elif cmd_type == 'exit':
            result = 'exit'
        else:
            raise ValueError(f'not supported command {cmd_type}')
        #  Send reply back to client
        socket.send(f'{result}'.encode('utf-8'))
        if result == 'exit':
            break

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print('starting client')
        start_client()
    else:
        print('starting server')
        start_server()