#!/usr/bin/env python3

"""Spike: confirm PX4 SITL telemetry is readable of MAVSDK. Not the real 
VehicleState producer -- that comes in Day 2 Commit 1."""

import asyncio

from mavsdk import System


async def main() -> None:
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    print("Waiting for drone conncetion...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to PX4 SITL")
            break

    asyncio.create_task(print_position(drone))
    asyncio.create_task(print_heading(drone))
    asyncio.create_task(print_battery(drone))

    await asyncio.sleep(30)

async def print_position(drone: System) -> None:
    async for position in drone.telemetry.position():
        print(
            f"position: lat={position.latitude_deg:.6f} "
            f"lon={position.longitude_deg:.6f} "
            f"alt={position.relative_altitude_m:.1f}m"
        )

async def print_heading(drone: System) -> None:
    async for attitude in drone.telemetry.attitude_euler():
        print(f"heading (yaw): {attitude.yaw_deg:.1f} deg")

async def print_battery(drone: System) -> None:
    async for battery in drone.telemetry.battery():
        print(f"battery:  {battery.remaining_percent:.1f}%")

if __name__ == "__main__":
    asyncio.run(main())