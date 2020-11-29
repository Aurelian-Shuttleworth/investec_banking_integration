from datetime import datetime, timedelta
import requests
from requests import auth
import json


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class AuthorizationBearer(requests.auth.AuthBase):
    def __init__(self, access_token):
        self.access_token = access_token

    def __call__(self, request):
        request.headers["Authorization"] = f"Bearer {self.access_token}"
        return request


class Client(metaclass=Singleton):
    """
    Singleton based class instance.
    Input:
        - token:
    """

    def __init__(self, client_id, client_secret):

        if not client_id or not client_secret:
            raise ValueError("To build a token the client_id and client_secret will be required.")

        self._token = None
        self.token = requests.auth.HTTPBasicAuth(client_id, client_secret)

        self._access_token = None
        self._expires_in = None  # lifetime in seconds, 3600 == 1 hour.
        self._token_expires = datetime.now()

        # urls data
        self._https = "https://"
        self._host = "openapi.investec.com"
        self._domain = "identity"
        self._version = "v2"
        self.auth_url = None

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    @property
    def expires_in(self):
        return self._expires_in

    @property
    def token_expires(self):
        return self._token_expires

    @expires_in.setter
    def expires_in(self, value):
        if value is not None:
            self._expires_in = value
            self._token_expires = datetime.now() + timedelta(seconds=value)

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    def _authentication(self):
        """Does oauth2 authentication, uses the token as the initial Basic auth api key."""
        if self.token_expires - timedelta(seconds=30) > datetime.now():
            return

        if self.auth_url is None:
            self.auth_url = f"{self._https}{self._host}/{self._domain}/{self._version}/oauth2/token"

        response = self.post(
            url=self.auth_url,
            headers=self._basic_header(),
            authorization=self.token,
        )

        self.access_token = json.loads(response.text).get("access_token")  # have a none base exception.
        self.expires_in = response.json().get("expires_in")

    @staticmethod
    def _basic_header():
        return {
            "content-type": "application/x-www-form-urlencoded",
        }

    @staticmethod
    def _bearer_header():
        return {
            "content-type": "application/json",
        }

    @staticmethod
    def post(url, headers, authorization):
        """Make a post request."""

        return requests.post(
            url=url,
            headers=headers,
            data="grant_type=client_credentials&scope=accounts",
            auth=authorization,
        )

    def get(self, url, headers):
        """Make a get request."""
        self._authentication()

        return requests.get(
            url=url,
            headers=headers,
            auth=AuthorizationBearer(self._access_token)
        )


class InvestecClient(Client):
    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)

        self.requests_lookup = [
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

    def _build_request_accounts(self, **kwargs):
        """
        GET /za/pb/v1/accounts
        /za/pb/v1/accounts
        """
        url = f"{self.https}{self.host}/{self.base}/{self.accounts}"

        try:
            response = self.get(
                url=url,
                headers=self._bearer_header()
            )
        except Exception as e:
            return e
        else:
            if response.status_code == 200:
                return json.loads(response.text)

    def _build_request_account_transactions(self, **kwargs):
        """
        GET /za/pb/v1/accounts{accountId}/transactions?fromDate={fromDate}&toDate={toDate}&transactionType={transactionType}
        required: accountId
        params: fromDate, toDate, transactionType
        """
        if "accountId" in kwargs:
            try:
                url = f"{self.https}{self.host}/{self.base}/{self.accounts}/{kwargs.get('accountId')}/transactions"
                response = self.get(
                    url=url,
                    headers=self._bearer_header()
                )
            except Exception as e:
                return e
            else:
                if response.status_code == 200:
                    return json.loads(response.text)

    def _build_request_account_balance(self, **kwargs):
        """
        GET /za/pb/v1/accounts{accountId}/balance
        """
        if "accountId" in kwargs:
            try:
                url = f"{self.https}{self.host}/{self.base}/{self.accounts}/{kwargs.get('accountId')}/balance"
                response = self.get(
                    url=url,
                    headers=self._bearer_header()
                )
            except Exception as e:
                return e
            else:
                if response.status_code == 200:
                    return json.loads(response.text)

    def access_bank(self, destination, **kwargs):
        """
        destination keywords
            - accounts
            - account_transactions
            - account_balance
        """
        if destination in self.requests_lookup:
            return getattr(self, f"_build_request_{destination}")(**kwargs)


