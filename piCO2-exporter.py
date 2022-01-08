#!/usr/bin/env python

import logging
from time import sleep
from threading import Event
import time
from prometheus_client import start_http_server, REGISTRY
from scd30_i2c import SCD30

from collector import Collector

event = Event()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    try:
        scd30 = SCD30()
    except PermissionError:
        logger.fatal('No captor available')
        quit()

    scd30.set_measurement_interval(2)
    scd30.start_periodic_measurement()

    time.sleep(2)

    REGISTRY.register(Collector(scd30, logger))

    start_http_server(9983)

    while True:
        try:
            sleep(10)
        except KeyboardInterrupt:
            event.set()
            break
