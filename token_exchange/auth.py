import requests
from furl import furl
from requests.auth import AuthBase
from rest_framework.request import Request

from .models import TokenExchangeConfiguration
from .signals import storage

# Docs https://www.keycloak.org/docs/latest/securing_apps/#_token-exchange
GRANT_TYPE = "urn:ietf:params:oauth:grant-type:token-exchange"


class TokenAccessAuth(AuthBase):
    def __call__(self, request: Request):
        config = TokenExchangeConfiguration.objects.filter(
            service__url=request.url
        ).first()

        if not config:
            return request

        # Perform token exchange
        exchange_url = furl(config.keycloak_base_url).set(
            {
                "grant_type": GRANT_TYPE,
                "subject_token": storage.access_token,
                "client_id": config.client_id,
                "client_secret": config.client_secret,
                "audience": config.audience,
            }
        )

        response = requests.post(
            exchange_url, headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        data = response.json()

        self.token = data["access_token"]
        # TODO find out header name
        request.headers["haal-centraal-header-TODO"] = self.token
        return request
