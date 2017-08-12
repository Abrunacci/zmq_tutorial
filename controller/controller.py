#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Standard lib imports
import time
import random
# Third Party imports
import threading
# BITSON imports
from logger import logger
from .handlers import ControllerHandler


class Controller:
    def __init__(self):
        self.handler = ControllerHandler()

    def run(self):
        self.handler.listen_to_requests()
        self.handler.start_publisher()
        while True:
            pass
