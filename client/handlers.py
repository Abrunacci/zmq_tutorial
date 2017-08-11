# -*- coding: utf-8 -*-
# Standard lib imports

# Third Party imports
import time
import zmq
# BITSON imports
from logger import logger
from constants import REPLIER_PORT
from constants import SERVER_IP
from .subscriber import SubscriberThread
from .requester import RequesterThread


class ClientHandler:
    def __init__(self):
        self.logger = logger
        self._ctx = zmq.Context()
        self.req = None
        self.sub = None
        self.mac = '1c:87:2c:d0:00:5e'
        self.command_request = {
            '10': self.ask_configuration,
            '22': self.keep_alive,
        }
        self.set_connections()

    def set_connections(self):
        self.req = RequesterThread(handler=self)
        self.sub = SubscriberThread(handler=self, default_filter=self.mac)
        self.start_subscriber()

    def start_subscriber(self):
        self.sub.start()

    def create_socket(self, type_):
        return self._ctx.socket(getattr(zmq, type_))

    def send_keep_alive(self):
        while True:
            self.keep_alive()
            time.sleep(5)

    def keep_alive(self):
        self.req.requester.send_command([b'22'])

    def ask_configuration(self):
        self.logger.info('Asking for configuration')
        self.req.requester.send_command([b'10'])

    def process_responses(self, response):
        if response['cmd'] != "00":
            self.logger.info('Response received: %s' % response)
        else:
            self.logger.debug('Response received: %s' % response)
