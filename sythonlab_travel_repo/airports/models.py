from dataclasses import dataclass
from typing import Optional

from sythonlab_travel_repo.airports.enums import AirportType
from sythonlab_travel_repo.core.enums import Continent


@dataclass
class Airport:
    id: int
    icao_code: str
    airport_type: AirportType
    name: str
    latitude: float
    longitude: float
    elevation_ft: Optional[float]
    continent: Optional[Continent]
    iso_country: Optional[str]
    iso_region: Optional[str]
    city: Optional[str]
    scheduled_service: bool
    gps_code: Optional[str]
    iata_code: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> "Airport":
        return cls(
            id=data["id"],
            icao_code=data["ident"],
            airport_type=AirportType(data["type"]),
            name=data["name"],
            latitude=data["latitude_deg"],
            longitude=data["longitude_deg"],
            elevation_ft=data.get("elevation_ft"),
            continent=Continent[data["continent"]] if data.get("continent") else None,
            iso_country=data.get("iso_country"),
            iso_region=data.get("iso_region"),
            city=data.get("municipality"),
            scheduled_service=data.get("scheduled_service") == "yes",
            gps_code=data.get("gps_code"),
            iata_code=data.get("iata_code"),
        )
