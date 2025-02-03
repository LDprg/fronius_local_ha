"""ConfigFlow for Fronius local."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_IP_ADDRESS, CONF_PASSWORD

from . import const as fl


class FroniusLocalFlow(config_entries.ConfigFlow, domain=fl.DOMAIN):
    """ConfigFlow class for Fronius local."""

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Async step user for configuaration."""
        errors = {}

        if user_input is not None:
            fl.LOGGER.info("Testing auth...")

            auth = fl.FroniusAuth()

            return self.async_create_entry(
                title="Fronius local",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_IP_ADDRESS): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )
