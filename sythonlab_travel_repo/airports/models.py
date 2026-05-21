"""Airport domain model."""

__author__ = "José Angel Alvarez Abraira"
__email__ = "sythonlab@gmail.com"

from dataclasses import dataclass
from typing import Optional

from sythonlab_travel_repo.airports.enums import AirportType
from sythonlab_travel_repo.core.enums import Continent


@dataclass
class Airport:
    """Represents a single airport entry.

    Attributes:
        id: Internal numeric identifier.
        icao_code: ICAO airport identifier (e.g. ``LEMD``).
        airport_type: Size/traffic classification.
        name: Full airport name.
        latitude: Latitude in decimal degrees.
        longitude: Longitude in decimal degrees.
        elevation_ft: Elevation above sea level in feet, if available.
        continent: Continent the airport is located in, if available.
        iso_country: ISO 3166-1 alpha-2 country code, if available.
        iso_region: ISO 3166-2 region code, if available.
        city: Municipality/city served by the airport, if available.
        scheduled_service: Whether the airport has scheduled commercial service.
        gps_code: GPS identifier, if available.
        iata_code: IATA airport code (e.g. ``MAD``), if available.
    """

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

    def __str__(self) -> str:
        return f"{self.iata_code} - {self.name}"

    @classmethod
    def from_dict(cls, data: dict) -> "Airport":
        """Construct an Airport from a raw JSON record.

        Args:
            data: Dictionary as loaded from the airports JSON file.

        Returns:
            A fully populated Airport instance.
        """
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
