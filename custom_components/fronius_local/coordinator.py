"""Coordinator for Fronisu local."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

if TYPE_CHECKING:
    from .data import FroniusConfigEntry


class FroniusCoordinator(DataUpdateCoordinator):
    """Fronius custom coordinator."""

    config_entry: FroniusConfigEntry

    async def _async_update_data(self) -> dict:
        """Update data via library."""
        return await self.config_entry.runtime_data.client.async_get_data()
