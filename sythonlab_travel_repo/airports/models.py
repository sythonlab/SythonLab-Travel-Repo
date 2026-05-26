"""Airport domain model."""

__author__ = "José Angel Alvarez Abraira"
__email__ = "sythonlab@gmail.com"

from dataclasses import dataclass, field
from typing import Optional

from sythonlab_travel_repo.airports.enums import AirportType
from sythonlab_travel_repo.core.enums import Continent, Language
from sythonlab_travel_repo.countries.models import LocalizedText


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
        country_name: Localized country name resolved from ``iso_country``, if available.
        country_flag: Flag emoji resolved from ``iso_country``, if available.
        locale: Display language used by ``label``. Not included in equality checks.
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
    country_name: Optional[LocalizedText] = field(default=None)
    country_flag: Optional[str] = field(default=None)
    locale: Language = field(default=Language.EN, compare=False)

    def __str__(self) -> str:
        return self.label

    @property
    def label(self) -> str:
        """Formatted display string.

        Example: ``[MAD] - 🇪🇸 Adolfo Suárez Madrid–Barajas Airport, España, ES``
        """
        code = self.iata_code or self.icao_code
        parts = [f"[{code}] -"]
        if self.country_flag:
            parts.append(self.country_flag)
        parts.append(self.name)
        suffix = []
        if self.country_name:
            suffix.append(self.country_name.get(self.locale))
        if self.iso_country:
            suffix.append(self.iso_country)
        if suffix:
            parts[-1] = parts[-1] + ","
            parts.append(", ".join(suffix))
        return " ".join(parts)

    @classmethod
    def from_dict(cls, data: dict) -> "Airport":
        """Construct an Airport from a raw JSON record.

        Args:
            data: Dictionary as loaded from the airports JSON file, optionally
                enriched with ``country_name`` (localized name dict) and
                ``country_flag`` keys by ``AirportService``.

        Returns:
            A fully populated Airport instance.
        """
        cn = data.get("country_name")
        country_name = LocalizedText(en=cn["en"], es=cn["es"]) if cn else None
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
            country_name=country_name,
            country_flag=data.get("country_flag"),
        )
