# -*- coding: utf-8 -*-
# Standard lib imports
import time
import json
import threading
# Third Party imports
import zmq
# BITSON imports
from logger import logger

MESSAGE_PORT = '5570'


class ServerHandler:
    def __init__(self):
        self.super()
        self.logger = logger
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.bind()

    def bind(self):
        self.logger.info('Binding connection: *:%s' % MESSAGE_PORT)
        self.publisher.bind('tcp://*:%s' % MESSAGE_PORT)

    def send_message(self, message=None):
        self.logger.info('Sending message: %s' % message)
        self.publisher.send_multipart(message)

    def run(self):
        for i in range(0, 100):
            message_lists = [[b'A', b'{"to": "A", "message": "This is the message A"}'],
                             [b'B', b'{"to": "B", "message": "This is the message B"}']]
            for message_list in message_lists:
                self.send_message(message_list)
            time.sleep(3)
        self.publisher.close()
        self.context.term()


class ServerThread(threading.Thread):
    def __init__(self):
        super().__init__(*args, **kwargs)