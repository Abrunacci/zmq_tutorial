# -*- coding: utf-8 -*-
# Standard lib imports
import time
import json
import threading
# Third Party imports
import zmq
# BITSON imports
from .replier import ReplierThread
from .publisher import PublisherThread


class ControllerHandler:
    def __init__(self):
        self._ctx = zmq.Context()
        self.rep = None
        self.pub = None

    def set_connections(self):
        self.rep = ReplierThread(handler=self)
        self.pub = PublisherThread(handler=self)

    def process_requests(self, cmd):
        self.rep.send_command(cmd)

    def listen_to_requests(self):
        self.rep.start()

    def create_socket(self, type_):
        return self._ctx.socket(getattr(zmq, type_))
