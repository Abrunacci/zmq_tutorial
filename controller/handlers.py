# -*- coding: utf-8 -*-
# Standard lib imports

# Third Party imports
import zmq
# BITSON imports
from logger import logger
from .replier import ReplierThread
from .publisher import PublisherThread


class ControllerHandler:
    def __init__(self):
        self._ctx = zmq.Context()
        self.rep = None
        self.pub = None
        self.logger = logger
        self.command_responses = {
            '10': self.send_configuration,
            '22': self.ack,
            '100': self.ack,
            '101': self.ack,  # Timeout Command (IDK)
            '102': self.ack,  # Anomaly Command (IDK)
            '103': self.validate_card,  # Validate Command (IDK)
        }
        self.set_connections()

    def set_connections(self):
        self.rep = ReplierThread(handler=self)
        self.pub = PublisherThread(handler=self)

    def start_publisher(self):
        self.pub.start()

    def process_requests(self, cmd):
        if cmd not in self.command_responses.keys():
            self.logger.error('Invalid command:%s' % cmd)
        self.rep.replier.send_command(self.command_responses[cmd]())

    def listen_to_requests(self):
        self.rep.start()

    def create_socket(self, type_):
        return self._ctx.socket(getattr(zmq, type_))

    @staticmethod
    def send_configuration():
        return [b'{"cmd":"10", "gate":"1", "position":"4", "state":"100"}']

    @staticmethod
    def ack():
        return [b'{"cmd":"00"}']

    @staticmethod
    def validate_card():
        return [b'{"cmd": "50", "access": "true"}']
