"""Constants for Fronius local."""

import json
import logging

import requests
from requests.auth import HTTPDigestAuth

DOMAIN = "fronius_local"

LOGGER = logging.getLogger(DOMAIN)

TIMEOUT = 9


class FroniusAuth:
    """Fronius auth class."""

    def __init__(self, url: str, passwd: str, user: str = "customer") -> None:
        """Init auth."""
        self.url = url
        self.user = user
        self.passwd = passwd

    def post(self, path: str) -> dict:
        """Request url from api."""
        res = requests.post(
            self.url + path,
            auth=HTTPDigestAuth(self.user, self.passwd),
            timeout=TIMEOUT,
        )
        return json.load(res.text)

    def get(self, path: str) -> dict:
        """Request url from api."""
        res = requests.get(
            self.url + path,
            auth=HTTPDigestAuth(self.user, self.passwd),
            timeout=TIMEOUT,
        )
        return json.load(res.text)
