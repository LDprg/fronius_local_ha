"""Sensor platform for Fronius local."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import Platform

from . import const as fl
from .entity import FroniusEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import FroniusCoordinator
    from .data import FroniusConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: FroniusConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    for k, v in entry.runtime_data.coordinator.data.items():
        fl.LOGGER.warn(str(k) + " ... " + str(v))
     
    async_add_entities(
        FroniusSensor(
            coordinator=entry.runtime_data.coordinator,
            unique_id=k,
            entity_description=SensorEntityDescription(
                key=k,
                name=v["name"],
            ),
        )
        for k, v in entry.runtime_data.coordinator.data.items()
        if v["type"] == Platform.SENSOR
    )


class FroniusSensor(FroniusEntity, SensorEntity):
    """integration_blueprint Sensor class."""

    def __init__(
        self,
        coordinator: FroniusCoordinator,
        unique_id: str,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator, unique_id)
        self.entity_description = entity_description

        self.native_unit_of_measurement = self.data()["unit"]

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.data()["value"]

    def data(self) -> dict | None:
        """Fetch entity data."""
        return self.coordinator.data[self.entity_description.key]
