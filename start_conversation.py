#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Standard lib imports
import time
import random
# Third Party imports
import threading
# BITSON imports
from logger import logger
from server.handlers import ServerHandler
from subscriber.handlers import SubscriberHandler

if __name__ == '__main__':
    logger.debug('Starting Server')
    server = ServerHandler()
    server_thread = threading.Thread(target=server.run)
    server_thread.name = 'Server-Thread'
    server_thread.daemon = True
    server_thread.start()
    logger.debug('Starting Subscriber')
    subscriber = SubscriberHandler()
    subscriber_thread = threading.Thread(target=subscriber.run)
    subscriber_thread.name = 'Subscriber-Thread'
    subscriber_thread.daemon = True
    subscriber_thread.start()
    subscriber.add_filter(new_filter='B')
    logger.debug('Changing filters in %s seconds' % 20)
    time.sleep(5)
    subscriber.remove_filter(old_filter='B')
    subscriber.add_filter(new_filter='A')
    while subscriber_thread.is_alive():
        seconds = random.randint(0, 30)
        logger.debug('Sending "END" message in %s seconds' % seconds)
        time.sleep(seconds)
        server.send_message(message=[b'A', b'{"message": "END"}'])
        time.sleep(1)
    logger.debug('Program finished')
