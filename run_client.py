#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Standard lib imports
import time
import random
# Third Party imports
import threading
# BITSON imports
from logger import logger
from client import Client


if __name__ == '__main__':
    try:
        client = Client()
        client.run()
    except KeyboardInterrupt:
        logger.info('Ctrl+C pressed. Program finished')
