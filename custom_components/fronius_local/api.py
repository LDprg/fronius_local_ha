"""Api for Fronius."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers import httpx_client

from . import auth
from . import const as fl

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


def is_meta(item: str) -> bool:
    """Check if string has a meta data marker."""
    return item.startswith("_") and item.endswith("_meta")


def meta(item: str) -> str:
    """Return meta string."""
    return "_" + item + "_meta"


def get_type(data: dict, key: str) -> Platform:
    """Get type of sensor."""
    if key in fl.FILTER:
        return Platform.SENSOR
    if (
        data[meta(key)]["writePermission"]["RoleCustomer"]
        and data[meta(key)]["displayType"] == "Integer"
    ):
        return Platform.NUMBER
    return Platform.SENSOR


class FroniusApiClient:
    """Fronius auth class."""

    def __init__(
        self,
        hass: HomeAssistant,
        url: str,
        passwd: str,
    ) -> None:
        """Init auth."""
        self.hass = hass
        self.url = url
        self.httpx = httpx_client.create_async_httpx_client(
            hass=hass,
            auth=auth.DigestAuthX("customer", passwd),
            base_url=url,
        )
        self.trans = None

    async def async_get_translation(self, lang: str) -> dict:
        """Return translated names."""
        if self.trans is None:
            self.trans = {}

        if self.trans.get(lang) is None:
            self.trans[lang] = await self.get(
                "http://192.168.0.42/app/assets/i18n/WeblateTranslations/config/"
                + lang
                + ".json"
            )

        return self.trans[lang]

    async def async_get_hwid(self) -> str:
        """Return Hardware ID."""
        return (await self.get("/status/version"))["hardwareId"]

    async def async_get_data(self) -> dict:
        """Update data."""
        battery = await self.get("/config/batteries")

        battery = {
            "conf_batteries_" + k: {
                "value": v,
                "type": get_type(battery, k),
                "name": (await self.async_get_translation(self.hass.config.language))[
                    "BATTERIES"
                ].get(k)
                or "CONF_BATTERIES_" + k,
                "id": k,
                "url": "/config/batteries",
                "unit": battery[meta(k)].get("unit"),
            }
            for (k, v) in battery.items()
            if not is_meta(k)
        }

        powerflow = await self.get("/status/powerflow")

        powerflow = {
            k: {
                "value": v,
                "type": Platform.SENSOR,
                "name": k,
                "id": k,
                "url": "/status/powerflow",
                "unit": None,
            }
            for (k, v) in powerflow.get("site").items()
        }

        timeofuse = await self.get("/config/timeofuse")

        timeofuse = {
            "timeuse_" + str(idx + 1): {
                "value": item.get("Active"),
                "type": Platform.SWITCH,
                "name": "Active " + str(idx + 1),
                "id": "timeuse_" + str(idx + 1),
                "nr": idx,
                "url": "/config/timeofuse",
                "unit": None,
            }
            for idx, item in enumerate(timeofuse.get("timeofuse"))
        }

        return battery | powerflow | timeofuse

    async def async_set_timeofuse(self, idx: int, active: bool) -> None:
        """Set timeofuse."""
        timeofuse = await self.get("/config/timeofuse")
        timeofuse = timeofuse.get("timeofuse")
        timeofuse[idx]["Active"] = active
        await self.post("/config/timeofuse", {"timeofuse": timeofuse})

    async def post(self, path: str, data: dict) -> dict:
        """Request url from api."""
        res = await self.httpx.post(
            path,
            json=data,
        )

        return res.json()

    async def get(self, path: str) -> dict:
        """Request url from api."""
        res = await self.httpx.get(
            path,
        )

        return res.json()
