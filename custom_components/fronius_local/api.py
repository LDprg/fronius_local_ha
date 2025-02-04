"""Api for Fronius."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers import httpx_client

from . import auth
from . import const as fl

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


class FroniusApiClient:
    """Fronius auth class."""

    def __init__(
        self,
        hass: HomeAssistant,
        url: str,
        passwd: str,
    ) -> None:
        """Init auth."""
        self.url = url
        self.httpx = httpx_client.create_async_httpx_client(
            hass=hass,
            auth=auth.DigestAuthX("customer", passwd),
            base_url=url,
        )

    async def async_get_data(self) -> dict:
        """Update data."""
        data = {}

        data["battery"] = await self.get("/config/batteries")

        return data

    async def post(self, path: str, data: dict) -> dict:
        """Request url from api."""
        res = await self.httpx.post(
            path,
            data=data,
        )

        fl.LOGGER.info(res.url)
        fl.LOGGER.info(res)
        return res.json()

    async def get(self, path: str) -> dict:
        """Request url from api."""
        res = await self.httpx.get(
            path,
        )

        fl.LOGGER.info(res.url)
        fl.LOGGER.info(res)
        return res.json()
