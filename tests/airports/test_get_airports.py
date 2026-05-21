import pytest

from sythonlab_travel_repo.airports.airports import AirportService
from sythonlab_travel_repo.airports.config import FilterConfig
from sythonlab_travel_repo.airports.enums import AirportType, AirportSortField
from sythonlab_travel_repo.airports.models import Airport
from sythonlab_travel_repo.core.enums import Continent, FilterType, SortOrder


@pytest.fixture(autouse=True)
def reset_config():
    AirportService.configure(filter_config=FilterConfig())
    yield
    AirportService.configure(filter_config=FilterConfig())


@pytest.fixture(scope="session", autouse=True)
def load_airports():
    AirportService.load()


class TestFilterById:
    def test_returns_matching_airport(self):
        results = AirportService.get_airports(airport_id=12243)
        assert len(results) == 1
        assert results[0].icao_code == "5A8"

    def test_returns_empty_when_not_found(self):
        assert AirportService.get_airports(airport_id=999999999) == []


class TestFilterByIataCode:
    def test_eq_exact_match(self):
        results = AirportService.get_airports(iata_code="JFK")
        assert len(results) == 1
        assert results[0].name == "John F Kennedy International Airport"

    def test_eq_case_insensitive(self):
        assert AirportService.get_airports(iata_code="jfk") == AirportService.get_airports(iata_code="JFK")

    def test_eq_no_partial_match(self):
        AirportService.configure(filter_config=FilterConfig(iata_code=FilterType.EQ))
        assert AirportService.get_airports(iata_code="JF") == []

    def test_contains_partial_match(self):
        AirportService.configure(filter_config=FilterConfig(iata_code=FilterType.CONTAINS))
        results = AirportService.get_airports(iata_code="JF")
        codes = [a.iata_code for a in results]
        assert "JFK" in codes


class TestFilterByName:
    def test_eq_exact_match(self):
        results = AirportService.get_airports(name="John F Kennedy International Airport")
        assert len(results) == 1

    def test_eq_case_insensitive(self):
        lower = AirportService.get_airports(name="john f kennedy international airport")
        upper = AirportService.get_airports(name="JOHN F KENNEDY INTERNATIONAL AIRPORT")
        assert lower == upper
        assert len(lower) == 1

    def test_eq_no_partial_match(self):
        AirportService.configure(filter_config=FilterConfig(name=FilterType.EQ))
        assert AirportService.get_airports(name="kennedy") == []

    def test_contains_partial_match(self):
        AirportService.configure(filter_config=FilterConfig(name=FilterType.CONTAINS))
        results = AirportService.get_airports(name="kennedy")
        assert any("Kennedy" in a.name for a in results)

    def test_contains_case_insensitive(self):
        AirportService.configure(filter_config=FilterConfig(name=FilterType.CONTAINS))
        lower = AirportService.get_airports(name="madrid")
        upper = AirportService.get_airports(name="MADRID")
        assert lower == upper


class TestFilterByAirportType:
    def test_large_airports(self):
        results = AirportService.get_airports(airport_type=AirportType.LARGE_AIRPORT)
        assert all(a.airport_type is AirportType.LARGE_AIRPORT for a in results)
        assert len(results) > 0

    def test_medium_airports(self):
        results = AirportService.get_airports(airport_type=AirportType.MEDIUM_AIRPORT)
        assert all(a.airport_type is AirportType.MEDIUM_AIRPORT for a in results)
        assert len(results) > 0


class TestFilterByContinent:
    def test_europe(self):
        results = AirportService.get_airports(continent=Continent.EU)
        assert all(a.continent is Continent.EU for a in results)
        assert len(results) > 0

    def test_asia(self):
        results = AirportService.get_airports(continent=Continent.AS)
        assert all(a.continent is Continent.AS for a in results)


class TestFilterByIsoCountry:
    def test_eq_exact(self):
        results = AirportService.get_airports(iso_country="US")
        assert all(a.iso_country == "US" for a in results)
        assert len(results) > 0

    def test_eq_case_insensitive(self):
        assert AirportService.get_airports(iso_country="us") == AirportService.get_airports(iso_country="US")

    def test_contains(self):
        AirportService.configure(filter_config=FilterConfig(iso_country=FilterType.CONTAINS))
        results = AirportService.get_airports(iso_country="U")
        countries = {a.iso_country for a in results}
        assert "US" in countries
        assert len(countries) > 1


class TestFilterByIsoRegion:
    def test_eq_exact(self):
        results = AirportService.get_airports(iso_region="US-AK")
        assert all(a.iso_region == "US-AK" for a in results)
        assert len(results) > 0

    def test_eq_case_insensitive(self):
        assert AirportService.get_airports(iso_region="us-ak") == AirportService.get_airports(iso_region="US-AK")

    def test_contains(self):
        AirportService.configure(filter_config=FilterConfig(iso_region=FilterType.CONTAINS))
        results = AirportService.get_airports(iso_region="US-")
        regions = {a.iso_region for a in results}
        assert len(regions) > 1


class TestFilterByCityName:
    def test_eq_exact(self):
        results = AirportService.get_airports(city_name="Paris")
        assert all(a.city == "Paris" for a in results)

    def test_eq_case_insensitive(self):
        assert AirportService.get_airports(city_name="paris") == AirportService.get_airports(city_name="PARIS")

    def test_contains_partial(self):
        AirportService.configure(filter_config=FilterConfig(city_name=FilterType.CONTAINS))
        results = AirportService.get_airports(city_name="new york")
        assert all("new york" in (a.city or "").lower() for a in results)

    def test_contains_case_insensitive(self):
        AirportService.configure(filter_config=FilterConfig(city_name=FilterType.CONTAINS))
        lower = AirportService.get_airports(city_name="london")
        upper = AirportService.get_airports(city_name="LONDON")
        assert lower == upper


class TestFilterByGpsCode:
    def test_eq_exact(self):
        results = AirportService.get_airports(gps_code="KJFK")
        assert len(results) == 1

    def test_eq_case_insensitive(self):
        assert AirportService.get_airports(gps_code="kjfk") == AirportService.get_airports(gps_code="KJFK")

    def test_contains(self):
        AirportService.configure(filter_config=FilterConfig(gps_code=FilterType.CONTAINS))
        results = AirportService.get_airports(gps_code="KJF")
        codes = [a.gps_code for a in results]
        assert "KJFK" in codes


class TestFilterByIcaoCode:
    def test_eq_exact(self):
        results = AirportService.get_airports(icao_code="KJFK")
        assert len(results) == 1

    def test_eq_case_insensitive(self):
        assert AirportService.get_airports(icao_code="kjfk") == AirportService.get_airports(icao_code="KJFK")

    def test_contains(self):
        AirportService.configure(filter_config=FilterConfig(icao_code=FilterType.CONTAINS))
        results = AirportService.get_airports(icao_code="KJF")
        idents = [a.icao_code for a in results]
        assert "KJFK" in idents


class TestCombinedFilters:
    def test_continent_and_type(self):
        results = AirportService.get_airports(
            continent=Continent.EU,
            airport_type=AirportType.LARGE_AIRPORT,
        )
        assert all(a.continent is Continent.EU and a.airport_type is AirportType.LARGE_AIRPORT for a in results)
        assert len(results) > 0

    def test_country_and_name_contains(self):
        AirportService.configure(filter_config=FilterConfig(name=FilterType.CONTAINS))
        results = AirportService.get_airports(iso_country="ES", name="madrid")
        assert len(results) > 0
        assert all(a.iso_country == "ES" for a in results)
        assert all("madrid" in a.name.lower() for a in results)

    def test_no_results_when_filters_conflict(self):
        results = AirportService.get_airports(continent=Continent.EU, iso_country="US")
        assert results == []


class TestSorting:
    def test_default_sort_by_name_asc(self):
        results = AirportService.get_airports(continent=Continent.EU)
        names = [a.name for a in results if a.name]
        assert names == sorted(names)

    def test_sort_by_name_desc(self):
        results = AirportService.get_airports(
            continent=Continent.EU,
            sort_by=AirportSortField.NAME,
            sort_order=SortOrder.DESC,
        )
        names = [a.name for a in results]
        assert names == sorted(names, reverse=True)

    def test_sort_by_elevation_desc_nulls_last(self):
        results = AirportService.get_airports(continent=Continent.EU, sort_by=AirportSortField.ELEVATION, sort_order=SortOrder.DESC)
        elevations = [a.elevation_ft for a in results]
        non_null = [e for e in elevations if e is not None]
        null_values = [e for e in elevations if e is None]
        assert non_null == sorted(non_null, reverse=True)
        assert elevations == non_null + null_values

    def test_sort_by_iata_asc_nulls_last(self):
        results = AirportService.get_airports(continent=Continent.SA, sort_by=AirportSortField.IATA_CODE)
        codes = [a.iata_code for a in results]
        non_null = [c for c in codes if c is not None]
        assert codes == non_null + [None] * codes.count(None)
        assert non_null == sorted(non_null)


class TestGetByCode:
    def test_get_by_iata_code(self):
        airport = AirportService.get_by_iata_code("JFK")
        assert isinstance(airport, Airport)
        assert airport.name == "John F Kennedy International Airport"

    def test_get_by_iata_code_case_insensitive(self):
        assert AirportService.get_by_iata_code("jfk") == AirportService.get_by_iata_code("JFK")

    def test_get_by_iata_code_not_found(self):
        assert AirportService.get_by_iata_code("XYZ") is None

    def test_get_by_icao_code(self):
        airport = AirportService.get_by_icao_code("KJFK")
        assert isinstance(airport, Airport)
        assert airport.iata_code == "JFK"

    def test_get_by_icao_code_case_insensitive(self):
        assert AirportService.get_by_icao_code("kjfk") == AirportService.get_by_icao_code("KJFK")

    def test_get_by_icao_code_not_found(self):
        assert AirportService.get_by_icao_code("ZZZZ") is None
