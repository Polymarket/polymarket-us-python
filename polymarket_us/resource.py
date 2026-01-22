"""Base resource classes."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from polymarket_us.async_client import AsyncPolymarketUS
    from polymarket_us.client import PolymarketUS


class APIResource:
    """Base class for API resources (sync)."""

    def __init__(self, client: PolymarketUS) -> None:
        self._client = client

    def _to_camel_case(self, snake_str: str) -> str:
        """Convert snake_case to camelCase."""
        components = snake_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    def _convert_params(
        self, params: Mapping[str, Any] | None
    ) -> dict[str, Any] | None:
        """Convert snake_case params to camelCase for the API."""
        if not params:
            return None
        result: dict[str, Any] = {}
        for key, value in params.items():
            camel_key = self._to_camel_case(key)
            if isinstance(value, dict):
                result[camel_key] = self._convert_params(value)
            else:
                result[camel_key] = value
        return result


class AsyncAPIResource:
    """Base class for API resources (async)."""

    def __init__(self, client: AsyncPolymarketUS) -> None:
        self._client = client

    def _to_camel_case(self, snake_str: str) -> str:
        """Convert snake_case to camelCase."""
        components = snake_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    def _convert_params(
        self, params: Mapping[str, Any] | None
    ) -> dict[str, Any] | None:
        """Convert snake_case params to camelCase for the API."""
        if not params:
            return None
        result: dict[str, Any] = {}
        for key, value in params.items():
            camel_key = self._to_camel_case(key)
            if isinstance(value, dict):
                result[camel_key] = self._convert_params(value)
            else:
                result[camel_key] = value
        return result
