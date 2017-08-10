# -*- coding: utf-8 -*-
# Standard lib imports
import time
import json
import threading
# Third Party imports
import zmq
# BITSON imports
from logger import logger
from constants import REPLIER_PORT


class RequesterHandler:
    def __init__(self):
        self.logger = logger
        self.context = zmq.context()
        self.replier = self.context.socket(zmq.REQ)
        self.bind()

    def bind(self):
        self.replier.bind('tcp://"*":%s' % REPLIER_PORT)

    def run(self):
        while True:
            msg = self.replier


class RequesterThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
