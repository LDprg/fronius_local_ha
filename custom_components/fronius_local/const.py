"""Constants for Fronius local."""

from __future__ import annotations

import logging

DOMAIN = "fronius_local"
ATTRIBUTION = "Data fetched from the local Fronius API"

LOGGER: logging.Logger = logging.getLogger(DOMAIN)

UPDATE_INTERVAL = 9
