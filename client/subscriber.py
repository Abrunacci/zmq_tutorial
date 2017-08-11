# -*- coding: utf-8 -*-
# Standard lib imports
import threading
# Third Party imports
import zmq
import json
# BITSON imports
from logger import logger
from constants import SERVER_IP, PUBLISHER_PORT


class Subscriber:
    def __init__(self, handler=None, default_filter=None):
        self.logger = logger
        self.handler = handler
        self.socket = self.handler.create_socket('SUB')
        self.default_filter = default_filter
        self.connect()

    def connect(self):
        self.logger.info("Connecting to: %s:%s" % (SERVER_IP, PUBLISHER_PORT))
        self.socket.connect('tcp://%s:%s' % (SERVER_IP, PUBLISHER_PORT))
        if self.default_filter:
            self.add_filter(new_filter=self.default_filter)

    def add_filter(self, new_filter=None):
        if not new_filter:
            self.logger.warning("Add filter needs an argument")
            return None
        self.logger.info("Adding filter: %s" % new_filter)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, new_filter)

    def remove_filter(self, old_filter=None):
        if not old_filter:
            self.logger.warning("Remove filter needs an argument")
            return None
        self.logger.info("Removing filter: %s" % old_filter)
        self.socket.setsockopt_string(zmq.UNSUBSCRIBE, old_filter)

    def listen_forever(self):
        while True:
            msg = self.socket.recv_multipart()[-1]
            msg = json.loads(msg.decode('utf-8'))
            self.logger.debug('Message received: %s' % msg)
            self.handler.process_responses(msg)


class SubscriberThread(threading.Thread):
    def __init__(self, handler=None, default_filter=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscriber = Subscriber(handler=handler, default_filter=default_filter)
        self.daemon = True
        self.name = 'Subscriber-Thread'

    def run(self):
        self.subscriber.listen_forever()
