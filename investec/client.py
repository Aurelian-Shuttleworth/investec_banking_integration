import requests
from base64 import b64encode


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class Client(metaclass=Singleton):
    """
    Singleton based class instance.
    Input:
        - token:
    """

    def __init__(self, token):
        # token and access_token data
        # timer check here to handle the token and access token.
        self.token = token
        self.access_token = None
        self.expires_in = None  # lifetime in seconds, 3600 == 1 hour.

        # headers
        self.headers = None

    def _authentication(self):
        """Does oauth2 authentication, uses the token as the initial Basic auth api key.

        https://openapi.investec.com/identity/v2/oauth2/token

        POST /identity/v2/oauth2/token

        client_id = None
        client_secret = None
        basic = b64encode(f"{client_id}:{client_secret}".encode("ascii")).decode()

        """
        # time check?

        headers = self._build_basic_header()
        response = self.post(destination="", headers=headers)
        data = response.json()

        self.access_token = data.get("access_token", None)  # have a none base exception.

        self.headers = self._build_bearer_header()

    def _build_header(self):
        # make a choice in the headers.
        pass

    def _build_basic_header(self):
        return {
            "Authorization": f"Basic {self.token}",
            "content-type": "application/x-www-form-urlencoded",
        }

    def _build_bearer_header(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "content-type": "application/json",
        }

    def post(self, destination, headers):
        """Make a post request."""

        url = getattr(self, destination)

        # get data as a conditional as well.

        return requests.post(
            url=url,
            headers=headers,
            data="",
        )

    def get(self, url):
        """Make a get request."""
        self._authentication()

        return requests.get(
            url=url,
            headers=self.headers,
        )


class InvestecClient(Client):
    def __init__(self, token):
        super().__init__(token)
        # singleton based, so will only have one instance, need to refresh if possible.

        self.destination_lookup = [
            "accounts",
            "account_transactions",
            "account_balance",
        ]

        self.https = "https://"
        self.host = "openapi.investec.com"
        self.domain = "za"
        self.api = "pb"
        self.version = "v1"
        self.accounts = "accounts"
        self.base = f"{self.domain}/{self.api}/{self.version}"

    def _build_destination_accounts(self, **kwargs):
        """
        GET /za/pb/v1/accounts
        """
        url = f"{self.https}{self.host}/{self.base}/{self.accounts}"

        try:
            response = self.get(url)
        except Exception as e:
            return e
        else:
            return response

    def _build_destination_account_transactions(self, **kwargs):
        """
        GET /za/pb/v1/accounts{accountId}/transactions?fromDate={fromDate}&toDate={toDate}&transactionType={transactionType}
        """
        if "accountId" in kwargs:
            try:
                url = f"{self.https}{self.host}/{self.base}/{self.accounts}{kwargs.get('accountId')}"
                response = self.get(url)
            except Exception as e:
                return e
            else:
                return response

        # required:
            # accountId

        # params:
            # fromDate
            # toDate
            # transactionType
        pass
        # try, except loop

    def _build_destination_account_balance(self, **kwargs):
        """
        GET /za/pb/v1/accounts{accountId}/balance
        """
        if "accountId" in kwargs:
            try:
                url = f"{self.https}{self.host}/{self.base}/{self.accounts}{kwargs.get('accountId')}/balance"
                response = self.get(url)
            except Exception as e:
                return e
            else:
                return response

    def access_banking(self, destination, **kwargs):
        """
        destination keywords
            - accounts
            - account_transactions
            - account_balance
        """
        if destination in self.destination_lookup:
            getattr(self, f"_build_destination_{destination}")(**kwargs)

