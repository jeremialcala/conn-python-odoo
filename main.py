# -*- coding: utf-8 -*-
import sys
import logging.config
import keyboard

import functools
import threading

from inspect import currentframe
from classes import Settings
from utils import configure_logging, timeit
from controller import on_message, get_amqp_connection

_set = Settings()

log = logging.getLogger(__name__)
logging.config.dictConfig(configure_logging())


@timeit
def get_help():
    """
    This get messages from a AMQP, This module use case is the data management with and Odoo server.

    Args:


    """


def process_messages(queue):
    log.info(f"Starting: {currentframe().f_code.co_name}")
    while True:
        _conn = get_amqp_connection()
        channel = _conn.channel()
        channel.queue_declare(queue=queue, auto_delete=False)
        channel.queue_bind(queue=queue, exchange=_set.amqp_exchange, routing_key=_set.amqp_routing_key)

        # This indicates the number of threads to be used by the message manager
        channel.basic_qos(prefetch_count=1)

        threads = []
        on_message_callback = functools.partial(on_message, args=(_conn, threads))
        channel.basic_consume(queue=queue, on_message_callback=on_message_callback)

        channel.start_consuming()

        # Wait for all to complete
        for thread in threads:
            thread.join()

        if keyboard.is_pressed('q'):
            channel.stop_consuming()
            break

    log.info(f"Ending: {currentframe().f_code.co_name}")


if __name__ == '__main__':
    configure_logging()
    log.info(f"Starting: {currentframe().f_code.co_name}")

    if "--help" in sys.argv or len(sys.argv) == 1:
        print(get_help.__doc__)
        sys.exit(0)

    arg_name = [arg for arg in sys.argv if "--" in arg]

    process_messages(_set.queue_name)
    log.info(f"Ending: {currentframe().f_code.co_name}")
    exit(0)
