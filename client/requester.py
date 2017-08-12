# -*- coding: utf-8 -*-
# Standard lib imports
import time
import json
import threading
# Third Party imports
import zmq
# BITSON imports
from logger import logger
from constants import REPLIER_PORT, SERVER_IP


class Requester:
    def __init__(self, handler=None):
        self.logger = logger
        self.handler = handler
        self.socket = self.handler.create_socket('REQ')
        self.connect()

    def connect(self):
        self.logger.info('Connecting to: %s:%s' % (SERVER_IP, REPLIER_PORT))
        self.socket.connect("tcp://%s:%s" % (SERVER_IP, REPLIER_PORT))

    def send_command(self, command=None):
        self.logger.debug('Sending command: %s' % command)
        self.socket.send_multipart(command)
        self.receive_message()

    def receive_message(self):
        msg = self.socket.recv_multipart()[-1]
        msg = json.loads(msg.decode('utf-8'))
        self.logger.debug('Message received: %s' % msg)
        return self.handler.process_responses(msg)


class RequesterThread(threading.Thread):
    def __init__(self, handler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger
        self.requester = Requester(handler=handler)
        self.daemon = True
        self.name = 'Replier-Thread'

