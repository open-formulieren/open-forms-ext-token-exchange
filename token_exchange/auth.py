import requests
from furl import furl
from requests.auth import AuthBase

from .models import TokenExchangeConfiguration
from .signals import storage

# Docs https://www.keycloak.org/docs/latest/securing_apps/#_token-exchange
GRANT_TYPE = "urn:ietf:params:oauth:grant-type:token-exchange"


class TokenAccessAuth(AuthBase):
    def __call__(self, request):
        config = TokenExchangeConfiguration.objects.filter(
            service__api_root__startswith=furl(request.url).origin
        ).first()

        if not config:
            return request

        # Perform token exchange
        exchange_url = furl(config.token_exchange_endpoint).set(
            {
                "grant_type": GRANT_TYPE,
                "subject_token": storage.access_token,
                "client_id": config.client_id,
                "client_secret": config.secret,
                "audience": config.audience,
            }
        )

        response = requests.post(
            exchange_url, headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        data = response.json()

        self.token = data["access_token"]
        # TODO find out header name
        request.headers["Authorization"] = self.token
        return request
