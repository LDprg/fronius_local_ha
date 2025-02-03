"""ConfigFlow for Fronius local."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_URL
from homeassistant.helpers import httpx_client

from . import const as fl
from .api import FroniusApiClient


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

            url = user_input[CONF_URL]
            passwd = user_input[CONF_PASSWORD]

            client = FroniusApiClient(
                url=url,
                passwd=passwd,
                httpx_client=httpx_client.create_async_httpx_client(self.hass),
            )

            hwid = await client.get_hwid()
            self.async_set_unique_id(hwid)

            fl.LOGGER.info("Auth valid!")

            return self.async_create_entry(
                title="Fronius local",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_URL): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )
