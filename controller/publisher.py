# -*- coding: utf-8 -*-
# Standard lib imports
import time
import json
import threading
# Third Party imports
import zmq
# BITSON imports
from logger import logger
from constants import PUBLISHER_PORT


class Publisher:
    def __init__(self, handler):
        self.logger = logger
        self.handler = handler
        self.publisher = self.handler.create_socket('PUB')
        self.bind()

    def bind(self):
        self.logger.info('Binding connection: *:%s' % PUBLISHER_PORT)
        self.publisher.bind('tcp://*:%s' % PUBLISHER_PORT)

    def send_message(self, message=None):
        self.logger.info('Sending message: %s' % message)
        self.publisher.send_multipart(message)

    @staticmethod
    def ask_for_command():
        return ""

    def send_message_forever(self):
        msg = [b"1c:87:2c:d0:00:5e"]
        cmd = dict()
        cmd["cmd"] = "30"
        msg.append(str.encode(json.dumps(cmd)))
        self.send_message(msg)


class PublisherThread(threading.Thread):
    def __init__(self, handler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server = Publisher(handler=handler)
        self.daemon = True
        self.name = 'Server-Thread'

    def run(self):
        while True:
            self.server.send_message_forever()
            time.sleep(10)

