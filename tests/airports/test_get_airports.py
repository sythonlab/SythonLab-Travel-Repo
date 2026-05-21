import pytest

from sythonlab_travel_repo.airports.airports import Airport
from sythonlab_travel_repo.airports.config import FilterConfig
from sythonlab_travel_repo.airports.enums import AirportType
from sythonlab_travel_repo.core.enums import Continent, FilterType


@pytest.fixture(autouse=True)
def reset_config():
    Airport.configure(filter_config=FilterConfig())
    yield
    Airport.configure(filter_config=FilterConfig())


@pytest.fixture(scope="session", autouse=True)
def load_airports():
    Airport.load()


class TestFilterById:
    def test_returns_matching_airport(self):
        results = Airport.get_airports(airport_id=12243)
        assert len(results) == 1
        assert results[0]["ident"] == "5A8"

    def test_returns_empty_when_not_found(self):
        assert Airport.get_airports(airport_id=999999999) == []


class TestFilterByIataCode:
    def test_eq_exact_match(self):
        results = Airport.get_airports(iata_code="JFK")
        assert len(results) == 1
        assert results[0]["name"] == "John F Kennedy International Airport"

    def test_eq_case_insensitive(self):
        assert Airport.get_airports(iata_code="jfk") == Airport.get_airports(iata_code="JFK")

    def test_eq_no_partial_match(self):
        Airport.configure(filter_config=FilterConfig(iata_code=FilterType.EQ))
        assert Airport.get_airports(iata_code="JF") == []

    def test_contains_partial_match(self):
        Airport.configure(filter_config=FilterConfig(iata_code=FilterType.CONTAINS))
        results = Airport.get_airports(iata_code="JF")
        codes = [a["iata_code"] for a in results]
        assert "JFK" in codes


class TestFilterByName:
    def test_eq_exact_match(self):
        results = Airport.get_airports(name="John F Kennedy International Airport")
        assert len(results) == 1

    def test_eq_case_insensitive(self):
        lower = Airport.get_airports(name="john f kennedy international airport")
        upper = Airport.get_airports(name="JOHN F KENNEDY INTERNATIONAL AIRPORT")
        assert lower == upper
        assert len(lower) == 1

    def test_eq_no_partial_match(self):
        Airport.configure(filter_config=FilterConfig(name=FilterType.EQ))
        assert Airport.get_airports(name="kennedy") == []

    def test_contains_partial_match(self):
        Airport.configure(filter_config=FilterConfig(name=FilterType.CONTAINS))
        results = Airport.get_airports(name="kennedy")
        assert any("Kennedy" in a["name"] for a in results)

    def test_contains_case_insensitive(self):
        Airport.configure(filter_config=FilterConfig(name=FilterType.CONTAINS))
        lower = Airport.get_airports(name="madrid")
        upper = Airport.get_airports(name="MADRID")
        assert lower == upper


class TestFilterByAirportType:
    def test_large_airports(self):
        results = Airport.get_airports(airport_type=AirportType.LARGE_AIRPORT)
        assert all(a["type"] == "large_airport" for a in results)
        assert len(results) > 0

    def test_medium_airports(self):
        results = Airport.get_airports(airport_type=AirportType.MEDIUM_AIRPORT)
        assert all(a["type"] == "medium_airport" for a in results)
        assert len(results) > 0


class TestFilterByContinent:
    def test_europe(self):
        results = Airport.get_airports(continent=Continent.EU)
        assert all(a["continent"] == "EU" for a in results)
        assert len(results) > 0

    def test_asia(self):
        results = Airport.get_airports(continent=Continent.AS)
        assert all(a["continent"] == "AS" for a in results)


class TestFilterByIsoCountry:
    def test_eq_exact(self):
        results = Airport.get_airports(iso_country="US")
        assert all(a["iso_country"] == "US" for a in results)
        assert len(results) > 0

    def test_eq_case_insensitive(self):
        assert Airport.get_airports(iso_country="us") == Airport.get_airports(iso_country="US")

    def test_contains(self):
        Airport.configure(filter_config=FilterConfig(iso_country=FilterType.CONTAINS))
        results = Airport.get_airports(iso_country="U")
        countries = {a["iso_country"] for a in results}
        assert "US" in countries
        assert len(countries) > 1


class TestFilterByIsoRegion:
    def test_eq_exact(self):
        results = Airport.get_airports(iso_region="US-AK")
        assert all(a["iso_region"] == "US-AK" for a in results)
        assert len(results) > 0

    def test_eq_case_insensitive(self):
        assert Airport.get_airports(iso_region="us-ak") == Airport.get_airports(iso_region="US-AK")

    def test_contains(self):
        Airport.configure(filter_config=FilterConfig(iso_region=FilterType.CONTAINS))
        results = Airport.get_airports(iso_region="US-")
        regions = {a["iso_region"] for a in results}
        assert len(regions) > 1


class TestFilterByCityName:
    def test_eq_exact(self):
        results = Airport.get_airports(city_name="Paris")
        assert all(a["municipality"] == "Paris" for a in results)

    def test_eq_case_insensitive(self):
        assert Airport.get_airports(city_name="paris") == Airport.get_airports(city_name="PARIS")

    def test_contains_partial(self):
        Airport.configure(filter_config=FilterConfig(city_name=FilterType.CONTAINS))
        results = Airport.get_airports(city_name="new york")
        assert all("new york" in (a["municipality"] or "").lower() for a in results)

    def test_contains_case_insensitive(self):
        Airport.configure(filter_config=FilterConfig(city_name=FilterType.CONTAINS))
        lower = Airport.get_airports(city_name="london")
        upper = Airport.get_airports(city_name="LONDON")
        assert lower == upper


class TestFilterByGpsCode:
    def test_eq_exact(self):
        results = Airport.get_airports(gps_code="KJFK")
        assert len(results) == 1

    def test_eq_case_insensitive(self):
        assert Airport.get_airports(gps_code="kjfk") == Airport.get_airports(gps_code="KJFK")

    def test_contains(self):
        Airport.configure(filter_config=FilterConfig(gps_code=FilterType.CONTAINS))
        results = Airport.get_airports(gps_code="KJF")
        codes = [a["gps_code"] for a in results]
        assert "KJFK" in codes


class TestFilterByIcaoCode:
    def test_eq_exact(self):
        results = Airport.get_airports(icao_code="KJFK")
        assert len(results) == 1

    def test_eq_case_insensitive(self):
        assert Airport.get_airports(icao_code="kjfk") == Airport.get_airports(icao_code="KJFK")

    def test_contains(self):
        Airport.configure(filter_config=FilterConfig(icao_code=FilterType.CONTAINS))
        results = Airport.get_airports(icao_code="KJF")
        idents = [a["ident"] for a in results]
        assert "KJFK" in idents


class TestCombinedFilters:
    def test_continent_and_type(self):
        results = Airport.get_airports(
            continent=Continent.EU,
            airport_type=AirportType.LARGE_AIRPORT,
        )
        assert all(a["continent"] == "EU" and a["type"] == "large_airport" for a in results)
        assert len(results) > 0

    def test_country_and_name_contains(self):
        Airport.configure(filter_config=FilterConfig(name=FilterType.CONTAINS))
        results = Airport.get_airports(iso_country="ES", name="madrid")
        assert len(results) > 0
        assert all(a["iso_country"] == "ES" for a in results)
        assert all("madrid" in a["name"].lower() for a in results)

    def test_no_results_when_filters_conflict(self):
        results = Airport.get_airports(
            continent=Continent.EU,
            iso_country="US",
        )
        assert results == []
