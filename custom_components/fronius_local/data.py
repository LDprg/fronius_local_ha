"""Custom types for Fronius local."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import FroniusApiClient
    from .coordinator import FroniusCoordinator


type FroniusConfigEntry = ConfigEntry[FroniusData]


@dataclass
class FroniusData:
    """Data for the Fronius local."""

    client: FroniusApiClient
    coordinator: FroniusCoordinator
    integration: Integration
