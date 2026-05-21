import pytest

from sythonlab_travel_repo.countries.config import CountryFilterConfig
from sythonlab_travel_repo.countries.countries import CountryService
from sythonlab_travel_repo.countries.enums import CountrySortField
from sythonlab_travel_repo.countries.models import Country, LocalizedText
from sythonlab_travel_repo.core.enums import FilterType, Language, SortOrder


@pytest.fixture(autouse=True)
def reset_config():
    CountryService.configure(filter_config=CountryFilterConfig())
    yield
    CountryService.configure(filter_config=CountryFilterConfig())


@pytest.fixture(scope="session", autouse=True)
def load_countries():
    CountryService.load()


class TestGetByAlpha2:
    def test_returns_correct_country(self):
        country = CountryService.get_by_alpha2("ES")
        assert isinstance(country, Country)
        assert country.name.en == "Spain"
        assert country.name.es == "España"
        assert country.alpha_2 == "ES"
        assert country.alpha_3 == "ESP"

    def test_case_insensitive(self):
        assert CountryService.get_by_alpha2("es") == CountryService.get_by_alpha2("ES")

    def test_returns_none_when_not_found(self):
        assert CountryService.get_by_alpha2("XX") is None

    def test_returns_country_with_flag(self):
        country = CountryService.get_by_alpha2("US")
        assert country.flag == "🇺🇸"

    def test_returns_country_with_nationality(self):
        country = CountryService.get_by_alpha2("FR")
        assert isinstance(country.nationality, LocalizedText)
        assert country.nationality.en == "French"
        assert country.nationality.es == "Francés/a"

    def test_locale_from_config(self):
        CountryService.configure(filter_config=CountryFilterConfig(), locale=Language.ES)
        country = CountryService.get_by_alpha2("ES")
        assert str(country) == "España"

    def test_locale_default_en(self):
        country = CountryService.get_by_alpha2("ES")
        assert str(country) == "Spain"


class TestGetByAlpha3:
    def test_returns_correct_country(self):
        country = CountryService.get_by_alpha3("ESP")
        assert isinstance(country, Country)
        assert country.alpha_2 == "ES"

    def test_case_insensitive(self):
        assert CountryService.get_by_alpha3("esp") == CountryService.get_by_alpha3("ESP")

    def test_returns_none_when_not_found(self):
        assert CountryService.get_by_alpha3("XXX") is None

    def test_locale_from_config(self):
        CountryService.configure(filter_config=CountryFilterConfig(), locale=Language.ES)
        country = CountryService.get_by_alpha3("JPN")
        assert str(country) == "Japón"


class TestFilterByNameEnglish:
    def test_eq_exact(self):
        results = CountryService.get_countries(name="Spain")
        assert len(results) == 1
        assert results[0].alpha_2 == "ES"

    def test_eq_case_insensitive(self):
        lower = CountryService.get_countries(name="spain")
        upper = CountryService.get_countries(name="SPAIN")
        assert lower == upper

    def test_eq_no_partial_match(self):
        assert CountryService.get_countries(name="Spa") == []

    def test_contains_partial_match(self):
        CountryService.configure(filter_config=CountryFilterConfig(name=FilterType.CONTAINS))
        results = CountryService.get_countries(name="land")
        names = [c.name.en for c in results]
        assert any("land" in n.lower() for n in names)
        assert len(results) > 1

    def test_contains_case_insensitive(self):
        CountryService.configure(filter_config=CountryFilterConfig(name=FilterType.CONTAINS))
        lower = CountryService.get_countries(name="republic")
        upper = CountryService.get_countries(name="REPUBLIC")
        assert lower == upper


class TestFilterByNameSpanish:
    def test_eq_exact(self):
        CountryService.configure(filter_config=CountryFilterConfig(), locale=Language.ES)
        results = CountryService.get_countries(name="España")
        assert len(results) == 1
        assert results[0].alpha_2 == "ES"

    def test_eq_case_insensitive(self):
        CountryService.configure(filter_config=CountryFilterConfig(), locale=Language.ES)
        lower = CountryService.get_countries(name="españa")
        upper = CountryService.get_countries(name="ESPAÑA")
        assert lower == upper

    def test_contains_partial_match(self):
        CountryService.configure(filter_config=CountryFilterConfig(name=FilterType.CONTAINS), locale=Language.ES)
        results = CountryService.get_countries(name="rep")
        assert all("rep" in c.name.es.lower() for c in results)
        assert len(results) > 1


class TestFilterByNationality:
    def test_eq_english(self):
        results = CountryService.get_countries(nationality="French")
        assert len(results) == 1
        assert results[0].alpha_2 == "FR"

    def test_eq_spanish(self):
        CountryService.configure(filter_config=CountryFilterConfig(), locale=Language.ES)
        results = CountryService.get_countries(nationality="Español/a")
        assert len(results) == 1
        assert results[0].alpha_2 == "ES"

    def test_contains_english(self):
        CountryService.configure(filter_config=CountryFilterConfig(nationality=FilterType.CONTAINS))
        results = CountryService.get_countries(nationality="ian")
        assert all("ian" in (c.nationality.en or "").lower() for c in results)
        assert len(results) > 1

    def test_null_nationality_not_returned(self):
        results = CountryService.get_countries(nationality="anything")
        for c in results:
            assert c.nationality is not None


class TestFilterByAlpha2:
    def test_eq_exact(self):
        results = CountryService.get_countries(alpha_2="US")
        assert len(results) == 1
        assert results[0].name.en == "United States"

    def test_eq_case_insensitive(self):
        assert CountryService.get_countries(alpha_2="us") == CountryService.get_countries(alpha_2="US")

    def test_contains(self):
        CountryService.configure(filter_config=CountryFilterConfig(alpha_2=FilterType.CONTAINS))
        results = CountryService.get_countries(alpha_2="U")
        codes = [c.alpha_2 for c in results]
        assert "US" in codes
        assert len(results) > 1


class TestFilterByAlpha3:
    def test_eq_exact(self):
        results = CountryService.get_countries(alpha_3="USA")
        assert len(results) == 1
        assert results[0].alpha_2 == "US"

    def test_eq_case_insensitive(self):
        assert CountryService.get_countries(alpha_3="usa") == CountryService.get_countries(alpha_3="USA")

    def test_contains(self):
        CountryService.configure(filter_config=CountryFilterConfig(alpha_3=FilterType.CONTAINS))
        results = CountryService.get_countries(alpha_3="US")
        codes = [c.alpha_3 for c in results]
        assert "USA" in codes


class TestSortingEnglish:
    def test_default_sort_by_name_asc_en(self):
        results = CountryService.get_countries()
        names = [c.name.en for c in results]
        assert names == sorted(names)

    def test_sort_by_name_desc_en(self):
        results = CountryService.get_countries(sort_by=CountrySortField.NAME, sort_order=SortOrder.DESC)
        names = [c.name.en for c in results]
        assert names == sorted(names, reverse=True)

    def test_sort_by_alpha2_asc(self):
        results = CountryService.get_countries(sort_by=CountrySortField.ALPHA_2)
        codes = [c.alpha_2 for c in results]
        assert codes == sorted(codes)

    def test_sort_by_alpha3_desc(self):
        results = CountryService.get_countries(sort_by=CountrySortField.ALPHA_3, sort_order=SortOrder.DESC)
        codes = [c.alpha_3 for c in results]
        assert codes == sorted(codes, reverse=True)


class TestSortingSpanish:
    def test_sort_by_name_asc_es(self):
        CountryService.configure(filter_config=CountryFilterConfig(), locale=Language.ES)
        results = CountryService.get_countries(sort_by=CountrySortField.NAME, sort_order=SortOrder.ASC)
        names = [c.name.es for c in results]
        assert names == sorted(names)

    def test_sort_by_name_desc_es(self):
        CountryService.configure(filter_config=CountryFilterConfig(), locale=Language.ES)
        results = CountryService.get_countries(sort_by=CountrySortField.NAME, sort_order=SortOrder.DESC)
        names = [c.name.es for c in results]
        assert names == sorted(names, reverse=True)

    def test_sort_by_nationality_asc_es(self):
        CountryService.configure(filter_config=CountryFilterConfig(), locale=Language.ES)
        results = CountryService.get_countries(sort_by=CountrySortField.NATIONALITY, sort_order=SortOrder.ASC)
        non_null = [c.nationality.es for c in results if c.nationality]
        assert non_null == sorted(non_null)

    def test_sort_nationality_nulls_last(self):
        results = CountryService.get_countries(sort_by=CountrySortField.NATIONALITY)
        nationalities = [c.nationality for c in results]
        null_start = next((i for i, n in enumerate(nationalities) if n is None), len(nationalities))
        assert all(n is None for n in nationalities[null_start:])

    def test_locale_applied_to_str(self):
        CountryService.configure(filter_config=CountryFilterConfig(), locale=Language.ES)
        results = CountryService.get_countries(sort_by=CountrySortField.NAME, sort_order=SortOrder.ASC)
        assert str(results[0]) == results[0].name.es


class TestCombinedFilters:
    def test_name_contains_and_alpha2_contains(self):
        CountryService.configure(filter_config=CountryFilterConfig(
            name=FilterType.CONTAINS,
            alpha_2=FilterType.CONTAINS,
        ))
        results = CountryService.get_countries(name="united", alpha_2="U")
        assert len(results) > 0
        assert all("united" in c.name.en.lower() for c in results)
        assert all("U" in c.alpha_2 for c in results)

    def test_no_results_when_filters_conflict(self):
        results = CountryService.get_countries(alpha_2="ES", alpha_3="USA")
        assert results == []
