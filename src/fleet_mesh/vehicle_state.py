from dataclasses import dataclass


@dataclass
class VehicleState:
    domain: str
    id: str
    lat: float
    lon: float
    alt_m: float
    heading_deg: float
    battery_pct: float
    status: str
    timestamp: float