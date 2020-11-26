import requests


class AbstractAuth:

    def __init__(self, token):
        self.token = token

        self.headers = None
        self.host = "openapi.investec.com"
        self.domain = "za"
        self.api = "pb"
        self.version = "v1"
        self.accounts = "accounts"
        self.balance = "accounts{accountId}/balance"

    def _build_header(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "content-type": "application/json",
        }

    async def get(self, url):
        """Make a get request."""
        self.headers = self._build_header()

        return requests.get(
            url=f"{self.host}/{self.domain}/{self.api}/{self.version}/{url}",
            headers=self.headers,
        )
