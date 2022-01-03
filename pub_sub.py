import zmq
print(zmq.__version__)
import sys

def start_sub():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt(zmq.SUBSCRIBE, b'2333')

    for _ in range(10):
        msg = socket.recv()
        topic, data = msg.split()
        print(f'topic:{topic}, data:{data}')

def start_pub():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")
    topic = 2333
    idx = 0
    while True:
        msg = b'%d %d'% (topic, idx)
        socket.send(msg)
        idx += 1

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print('starting sub')
        start_sub()
    else:
        print('starting pub')
        start_pub()