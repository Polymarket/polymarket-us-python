"""Account resource."""

from polymarket_us.resource import APIResource, AsyncAPIResource
from polymarket_us.types import GetAccountBalancesResponse


class Account(APIResource):
    """Account API resource."""

    def balances(self) -> GetAccountBalancesResponse:
        """Get account balances.

        Returns:
            Response containing account balances
        """
        return self._client.get("/v1/account/balances", authenticated=True)


class AsyncAccount(AsyncAPIResource):
    """Account API resource (async)."""

    async def balances(self) -> GetAccountBalancesResponse:
        """Get account balances.

        Returns:
            Response containing account balances
        """
        return await self._client.get("/v1/account/balances", authenticated=True)
