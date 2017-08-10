# -*- coding: utf-8 -*-
# Standard lib imports

# Third Party imports
import zmq
import json
# BITSON imports
from logger import logger

SERVER_IP = '192.168.1.6'
MESSAGE_PORT = '5570'


class SubscriberHandler:
    def __init__(self, **kwargs):
        self.logger = logger
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.client = self.context.socket(zmq.REQ)
        self.connect()

    def connect(self):
        self.logger.info("Connecting to: %s:%s" % (SERVER_IP, MESSAGE_PORT))
        self.subscriber.connect('tcp://%s:%s' % (SERVER_IP, MESSAGE_PORT))
        # self.client.connect('tcp://%s:%s' % (SERVER_IP, MESSAGE_PORT))

    def add_filter(self, new_filter=None):
        self.logger.info("Adding filter: %s" % new_filter)
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, new_filter)

    def remove_filter(self, old_filter=None):
        self.logger.info("Removing filter: %s" % old_filter)
        self.subscriber.setsockopt_string(zmq.UNSUBSCRIBE, old_filter)

    def run(self):
        self.logger.info("Starting Subscriber")
        self.logger.debug("Start loop")
        nbr = 0
        while True:
            msg = self.subscriber.recv_multipart()[-1]
            msg = json.loads(msg.decode('utf-8'))
            self.logger.info('Message "%s" received' % msg['message'])
            if msg['message'] == 'END':
                self.logger.info('Ending Subscriber')
                break
            nbr += 1

        self.logger.info('Received %d updates' % nbr)

