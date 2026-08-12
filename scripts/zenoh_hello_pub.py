#!/usr/bin/env python3

"""Spike: confirm zenoh-python pub/sub works on loopback."""

import time

import zenoh

with zenoh.open(zenoh.Config()) as session:
    with session.declare_publisher("demo/hello") as pub:
        count = 0
        while True:
            message = f"hello #{count}"
            print(f"publishing: {message}")
            pub.put(message)
            count += 1
            time.sleep(1)