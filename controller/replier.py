# -*- coding: utf-8 -*-
# Standard lib imports
import time
import json
import threading
# Third Party imports

# BITSON imports
from logger import logger
from constants import REPLIER_PORT


class Replier:
    def __init__(self, handler):
        self.logger = logger
        self.handler = handler
        self.socket = self.handler.create_socket('REP')
        self.bind()

    def bind(self):
        self.logger.info('Binding connection: *:%s' % REPLIER_PORT)
        self.socket.bind('tcp://*:%s' % REPLIER_PORT)

    def send_command(self, command=None):
        self.logger.info('Sending command: %s' % command)
        self.socket.send_multipart(command)

    def receive_message(self):
        msg = self.socket.recv_multipart()[-1]
        msg = msg.decode('utf-8')
        self.logger.info('Message received: %s' % msg)
        return self.handler.process_requests(msg)


class ReplierThread(threading.Thread):
    def __init__(self, handler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger
        self.replier = Replier(handler=handler)
        self.daemon = True
        self.name = 'Replier-Thread'

    def run(self):
        while True:
            self.replier.receive_message()

