"""Switch platform for Fronius local."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.const import Platform

from .entity import FroniusEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import FroniusCoordinator
    from .data import FroniusConfigEntry


async def async_setup_entry(
    _hass: HomeAssistant,
    entry: FroniusConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        FroniusSwitch(
            coordinator=entry.runtime_data.coordinator,
            unique_id=k,
            entity_description=SwitchEntityDescription(
                key=k,
                name=v["name"],
            ),
        )
        for k, v in entry.runtime_data.coordinator.data.items()
        if v["type"] == Platform.SWITCH
    )


class FroniusSwitch(FroniusEntity, SwitchEntity):
    """integration_blueprint Sensor class."""

    def __init__(
        self,
        coordinator: FroniusCoordinator,
        unique_id: str,
        entity_description: SwitchEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator, unique_id)
        self.entity_description = entity_description
        self.entity_id = "number." + unique_id

        self.extra_state_attributes = {"id": self.data()["id"]}

    @property
    def is_on(self) -> bool | None:
        """Return the native value of the sensor."""
        return self.data()["value"]

    async def async_turn_on(self, **_kwargs: any) -> None:
        """Turn the entity on."""
        await self.coordinator.config_entry.runtime_data.client.async_set_timeofuse(
            self.data()["nr"], True
        )

    async def async_turn_off(self, **_kwargs: any) -> None:
        """Turn the entity on."""
        await self.coordinator.config_entry.runtime_data.client.async_set_timeofuse(
            self.data()["nr"], False
        )

    def data(self) -> dict | None:
        """Fetch entity data."""
        return self.coordinator.data[self.entity_description.key]
