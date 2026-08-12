#!/usr/bin/env python3

"""Spike:  confrim zenoh-python pub/sub works on loopback."""

import zenoh

with zenoh.open(zenoh.Config()) as session:
    with session.declare_subscriber("demo/hello") as sub:
        print("listening on demo/hello...")
        for sample in sub:
            print(f"received:  {sample.payload.to_string()}")