import asyncio
import time

from mavsdk import System

from fleet_mesh.vehicle_state import VehicleState

PUBLISH_INTERVAL_S = 1.0


class AirNode:
    def __init__(self, vehicle_id: str, system_address: str = "udpin://0.0.0.0:14540"):
        self.vehicle_id = vehicle_id
        self.system_address = system_address
        self._lat = 0.0
        self._lon = 0.0
        self._alt_m = 0.0
        self._heading_deg = 0.0
        self._battery_pct = 0.0

    async def _track_position(self, drone: System) -> None:
        async for position in drone.telemetry.position():
            self._lat = position.latitude_deg
            self._lon = position.longitude_deg
            self._alt_m = position.relative_altitude_m

    async def _track_heading(self, drone: System) -> None:
        async for attitude in drone.telemetry.attitude_euler():
            self._heading_deg = attitude.yaw_deg

    async def _track_battery(self, drone: System) -> None:
        async for battery in drone.telemetry.battery():
            self._battery_pct = battery.remaining_percent

    async def states(self):
        drone = System()
        await drone.connect(system_address=self.system_address)

        async for conn_state in drone.core.connection_state():
            if conn_state.is_connected:
                break

        asyncio.create_task(self._track_position(drone))
        asyncio.create_task(self._track_heading(drone))
        asyncio.create_task(self._track_battery(drone))

        while True:
            yield VehicleState(
                domain="air",
                id=self.vehicle_id,
                lat=self._lat,
                lon=self._lon,
                alt_m=self._alt_m,
                heading_deg=self._heading_deg,
                battery_pct=self._battery_pct,
                status="nominal",
                timestamp=time.time(),
            )
            await asyncio.sleep(PUBLISH_INTERVAL_S)