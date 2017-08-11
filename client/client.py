#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Standard lib imports
import threading
# Third Party imports

# BITSON imports
from logger import logger
from .handlers import ClientHandler


class Client:
    def __init__(self):
        self.handler = ClientHandler()

    def run(self):
        self.handler.ask_configuration()
        keep_alive_thread = threading.Thread(target=self.handler.send_keep_alive)
        keep_alive_thread.daemon = True
        keep_alive_thread.name = 'Keep_Alive-Thread'
        keep_alive_thread.start()
        while True:
            pass
