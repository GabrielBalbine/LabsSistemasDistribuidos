import zmq
from time import time, sleep

context = zmq.Context()
pub = context.socket(zmq.PUB)
pub.connect("tcp://proxy:5555")

while True:
    topic = "time".encode("utf-8")
    topic2 = "hello".encode("utf-8")
    topic3 = "random".encode("utf-8")
    message = str(time()).encode("utf-8")
    pub.send_multipart([topic, message])
    pub.send_multipart([topic2, message])
    pub.send_multipart([topic3, message])
    sleep(1)


pub.close()
context.close()
