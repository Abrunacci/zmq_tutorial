# -*- coding: utf-8 -*-
# Standard lib imports
import threading
# Third Party imports
import zmq
import json
# BITSON imports
from logger import logger
from constants import SERVER_IP, PUBLISHER_PORT


class SubscriberHandler:
    def __init__(self, **kwargs):
        self.logger = logger
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.sync = self.context.socket(zmq.REQ)
        self.started = True
        self.connect()

    def connect(self):
        self.logger.info("Connecting to: %s:%s" % (SERVER_IP, PUBLISHER_PORT))
        self.subscriber.connect('tcp://%s:%s' % (SERVER_IP, PUBLISHER_PORT))

    def add_filter(self, new_filter=None):
        if not new_filter:
            self.logger.warning("Add filter needs an argument")
            return None
        self.logger.info("Adding filter: %s" % new_filter)
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, new_filter)

    def remove_filter(self, old_filter=None):
        if not old_filter:
            self.logger.warning("Remove filter needs an argument")
            return None
        self.logger.info("Removing filter: %s" % old_filter)
        self.subscriber.setsockopt_string(zmq.UNSUBSCRIBE, old_filter)

    def run(self):
        self.logger.info("Starting Subscriber")
        while self.started:
            msg = self.subscriber.recv_multipart()[-1]
            msg = json.loads(msg.decode('utf-8'))
            self.logger.info('Message "%s" received' % msg['message'])
            # self.process_command(msg['command'], msg['arguments'])
        self.logger.info("Starting Subscriber")


class SubscriberThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscriber = SubscriberHandler()
        self.daemon = True
        self.name = 'Server-Thread'

    def run(self):
        self.subscriber.run()
