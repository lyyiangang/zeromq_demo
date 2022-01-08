import zmq
import sys
import os
import time
import numpy as np
import cv2
sys.path.append(os.getcwd() + '/build')

from msg_pb2 import *

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5557")
socket.setsockopt_string(zmq.SUBSCRIBE, "")
time.sleep(1)

ocv_mat = OcvMat()
while True:
    t_start = time.time()
    raw_msg = socket.recv()
    ocv_mat.ParseFromString(raw_msg)
    img = np.frombuffer(ocv_mat.mat_data, dtype = np.uint8)
    img = img.reshape(ocv_mat.rows, ocv_mat.cols, ocv_mat.channels)
    fps = 1/(time.time() - t_start) 
    print(f'fps:{fps}')
    cv2.imshow('img', img)
    cv2.waitKey(1)