"""Api for Fronius."""

import httpx


class FroniusApiClient:
    """Fronius auth class."""

    def __init__(
        self,
        url: str,
        passwd: str,
        httpx_client: httpx,
        user: str = "customer",
    ) -> None:
        """Init auth."""
        self.url = url
        self.user = user
        self.passwd = passwd
        self.httpx = httpx_client

    async def get_hwid(self) -> str:
        """Return hardware id."""
        res = await self.get("/status/version")

        return res["hardwareId"]

    async def get_battery(self) -> dict:
        """Return battery status."""
        return await self.get("/config/batteries")

    async def set_battery(self, data: dict) -> dict:
        """Set battery config."""
        return await self.post("/config/batteries", data)

    async def post(self, path: str, data: dict) -> dict:
        """Request url from api."""
        res = await self.httpx.post(
            self.url + path,
            data=data,
            auth=httpx.DigestAuth(self.user, self.passwd),
        )
        return res.json()

    async def get(self, path: str) -> dict:
        """Request url from api."""
        res = await self.httpx.get(
            self.url + path,
            auth=httpx.DigestAuth(self.user, self.passwd),
        )
        return res.json()
