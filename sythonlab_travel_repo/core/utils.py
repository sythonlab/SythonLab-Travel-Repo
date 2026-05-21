"""Shared utility functions for the travel repository."""

__author__ = "José Angel Alvarez Abraira"
__email__ = "sythonlab@gmail.com"

from typing import Optional

from sythonlab_travel_repo.core.enums import FilterType


def match_str(field_value: Optional[str], query: str, filter_type: FilterType) -> bool:
    """Test whether a string field satisfies a query under the given filter strategy.

    Args:
        field_value: The value from the data record. Returns ``False`` if ``None``.
        query: The query string to match against.
        filter_type: ``EQ`` for exact match, ``CONTAINS`` for substring match.
            Both are case-insensitive.

    Returns:
        ``True`` if the field matches the query, ``False`` otherwise.
    """
    if field_value is None:
        return False
    if filter_type is FilterType.CONTAINS:
        return query.lower() in field_value.lower()
    return field_value.lower() == query.lower()
