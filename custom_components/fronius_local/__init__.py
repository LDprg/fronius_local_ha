"""Fronius local integration."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import CONF_PASSWORD, CONF_URL, Platform
from homeassistant.loader import async_get_loaded_integration

from . import const as fl
from .api import FroniusApiClient
from .coordinator import FroniusCoordinator
from .data import FroniusData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import FroniusConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.NUMBER,
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: FroniusConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = FroniusCoordinator(
        hass=hass,
        logger=fl.LOGGER,
        name=fl.DOMAIN,
        update_interval=timedelta(seconds=fl.UPDATE_INTERVAL),
    )

    entry.runtime_data = FroniusData(
        client=FroniusApiClient(
            hass=hass,
            url=entry.data[CONF_URL].strip(),
            passwd=entry.data[CONF_PASSWORD],
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: FroniusConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )


async def async_reload_entry(
    hass: HomeAssistant,
    entry: FroniusConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
