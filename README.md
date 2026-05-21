<p align="center">
  <img src="sythonlab_travel_repo/logo.png" alt="SythonLab" width="256" height="256"/>
</p>

# SythonLab Travel Repository

A Python library for querying airport and country data with filtering, sorting, and multilingual support.

---

## Installation

```bash
pip install sythonlab-travel-repo
```

---

## Modules

- **`airports`** — Query large and medium airports worldwide.
- **`countries`** — Query ISO 3166-1 countries with localized names and nationalities.

---

## Quick Start

### Airports

```python
from sythonlab_travel_repo.airports.airports import AirportService
from sythonlab_travel_repo.airports.config import FilterConfig
from sythonlab_travel_repo.airports.enums import AirportSortField
from sythonlab_travel_repo.core.enums import FilterType, SortOrder

# Load data once at startup
AirportService.load()

# Optional: configure filter strategies (default is EQ for all fields)
AirportService.configure(filter_config=FilterConfig(name=FilterType.CONTAINS))

# Query
results = AirportService.get_airports(
    name="Madrid",
    sort_by=AirportSortField.NAME,
    sort_order=SortOrder.ASC,
)

for airport in results:
    print(airport)  # "MAD - Adolfo Suárez Madrid–Barajas Airport"
```

### Countries

```python
from sythonlab_travel_repo.countries.countries import CountryService
from sythonlab_travel_repo.countries.config import CountryFilterConfig
from sythonlab_travel_repo.countries.enums import CountrySortField
from sythonlab_travel_repo.core.enums import FilterType, Language, SortOrder

# Load data once at startup
CountryService.load()

# Optional: configure filter strategies and display language
CountryService.configure(
    filter_config=CountryFilterConfig(name=FilterType.CONTAINS),
    locale=Language.ES,
)

# Query
results = CountryService.get_countries(
    name="rep",
    sort_by=CountrySortField.NAME,
    sort_order=SortOrder.ASC,
)

for country in results:
    print(country)  # prints name in Spanish
```

---

## API Reference

### `AirportService`

#### `AirportService.load()`
Loads the airport dataset from the bundled JSON file. Must be called once before any queries.

#### `AirportService.configure(*, filter_config)`
Sets the active filter configuration.

| Parameter | Type | Description |
|---|---|---|
| `filter_config` | `FilterConfig` | Per-field filter strategies. |

#### `AirportService.get_airports(**filters)`
Returns a list of `Airport` objects matching all supplied filters.

| Parameter | Type | Description |
|---|---|---|
| `airport_id` | `int` | Exact numeric ID. |
| `icao_code` | `str` | ICAO code (e.g. `LEMD`). |
| `airport_type` | `AirportType` | `MEDIUM_AIRPORT` or `LARGE_AIRPORT`. |
| `name` | `str` | Airport name. |
| `continent` | `Continent` | Continent enum value. |
| `iso_country` | `str` | ISO 3166-1 alpha-2 country code. |
| `iso_region` | `str` | ISO 3166-2 region code. |
| `city_name` | `str` | City/municipality name. |
| `gps_code` | `str` | GPS code. |
| `iata_code` | `str` | IATA code (e.g. `MAD`). |
| `sort_by` | `AirportSortField` | Field to sort by. Default: `NAME`. |
| `sort_order` | `SortOrder` | `ASC` or `DESC`. Default: `ASC`. |

#### `AirportService.get_by_iata_code(code)`
Returns the `Airport` matching the given IATA code, or `None`.

#### `AirportService.get_by_icao_code(code)`
Returns the `Airport` matching the given ICAO code, or `None`.

---

### `CountryService`

#### `CountryService.load()`
Loads the country dataset from the bundled JSON file. Must be called once before any queries.

#### `CountryService.configure(*, filter_config, locale)`
Sets the active filter configuration and display language.

| Parameter | Type | Description |
|---|---|---|
| `filter_config` | `CountryFilterConfig` | Per-field filter strategies. |
| `locale` | `Language` | Language for localized fields. Default: `Language.EN`. |

#### `CountryService.get_countries(**filters)`
Returns a list of `Country` objects matching all supplied filters.

| Parameter | Type | Description |
|---|---|---|
| `name` | `str` | Country name (matched in active locale). |
| `nationality` | `str` | Nationality/demonym (matched in active locale). |
| `alpha_2` | `str` | ISO 3166-1 alpha-2 code (e.g. `ES`). |
| `alpha_3` | `str` | ISO 3166-1 alpha-3 code (e.g. `ESP`). |
| `sort_by` | `CountrySortField` | Field to sort by. Default: `NAME`. |
| `sort_order` | `SortOrder` | `ASC` or `DESC`. Default: `ASC`. |

#### `CountryService.get_by_alpha2(code)`
Returns the `Country` matching the given alpha-2 code, or `None`.

#### `CountryService.get_by_alpha3(code)`
Returns the `Country` matching the given alpha-3 code, or `None`.

---

## Models

### `Airport`

| Field | Type | Description |
|---|---|---|
| `id` | `int` | Internal identifier. |
| `icao_code` | `str` | ICAO code. |
| `airport_type` | `AirportType` | Size classification. |
| `name` | `str` | Full airport name. |
| `latitude` | `float` | Latitude in decimal degrees. |
| `longitude` | `float` | Longitude in decimal degrees. |
| `elevation_ft` | `float \| None` | Elevation in feet. |
| `continent` | `Continent \| None` | Continent. |
| `iso_country` | `str \| None` | ISO country code. |
| `iso_region` | `str \| None` | ISO region code. |
| `city` | `str \| None` | City served. |
| `scheduled_service` | `bool` | Has scheduled commercial service. |
| `gps_code` | `str \| None` | GPS code. |
| `iata_code` | `str \| None` | IATA code. |

### `Country`

| Field | Type | Description |
|---|---|---|
| `id` | `int` | Internal identifier. |
| `name` | `LocalizedText` | Name in English and Spanish. |
| `alpha_2` | `str` | ISO 3166-1 alpha-2 code. |
| `alpha_3` | `str` | ISO 3166-1 alpha-3 code. |
| `flag` | `str` | Flag emoji. |
| `nationality` | `LocalizedText \| None` | Demonym in English and Spanish. |
| `locale` | `Language` | Active display language (set by the service). |

### `LocalizedText`

| Field | Type | Description |
|---|---|---|
| `en` | `str` | English text. |
| `es` | `str` | Spanish text. |

`localizedText.get(language)` returns the text in the requested language.

---

## Enumerations

### `FilterType`
| Value | Description |
|---|---|
| `EQ` | Exact case-insensitive match. |
| `CONTAINS` | Case-insensitive substring match. |

### `SortOrder`
| Value | Description |
|---|---|
| `ASC` | Ascending order. |
| `DESC` | Descending order. |

### `Language`
| Value | Description |
|---|---|
| `EN` | English. |
| `ES` | Spanish. |

### `AirportType`
| Value | Description |
|---|---|
| `MEDIUM_AIRPORT` | Medium-sized airport. |
| `LARGE_AIRPORT` | Large international airport. |

### `AirportSortField`
`ID`, `NAME`, `IATA_CODE`, `ICAO_CODE`, `COUNTRY`, `REGION`, `CITY`, `GPS_CODE`, `ELEVATION`

### `CountrySortField`
`ID`, `NAME`, `ALPHA_2`, `ALPHA_3`, `NATIONALITY`

### `Continent`
`AF`, `AS`, `EU`, `NA`, `OC`, `SA`

---

## Filter Configuration

Use `FilterConfig` / `CountryFilterConfig` to control how each field is matched:

```python
from sythonlab_travel_repo.airports.config import FilterConfig
from sythonlab_travel_repo.core.enums import FilterType

# Name uses substring match; all other fields use exact match
AirportService.configure(filter_config=FilterConfig(name=FilterType.CONTAINS))
```

```python
from sythonlab_travel_repo.countries.config import CountryFilterConfig

# Both name and nationality use substring match
CountryService.configure(
    filter_config=CountryFilterConfig(
        name=FilterType.CONTAINS,
        nationality=FilterType.CONTAINS,
    ),
    locale=Language.ES,
)
```

---

## Author

**José Angel Alvarez Abraira** — [sythonlab@gmail.com](mailto:sythonlab@gmail.com)  
GitHub: [sythonlab/SythonLab-Travel-Repo](https://github.com/sythonlab/SythonLab-Travel-Repo)
