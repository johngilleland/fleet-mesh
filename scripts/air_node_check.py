#!/usr/bin/env python3
import asyncio

from fleet_mesh.domains.air import AirNode


async def main() -> None:
    node = AirNode(vehicle_id="air-1")
    async for state in node.states():
        print(state)


if __name__ == "__main__":
    asyncio.run(main())