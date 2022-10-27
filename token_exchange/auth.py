import requests
from furl import furl
from openforms.authentication.registry import register as registry
from requests.auth import AuthBase
from zgw_consumers.models import Service

from .models import TokenExchangeConfiguration
from .signals import storage

# Docs https://www.keycloak.org/docs/latest/securing_apps/#_token-exchange
GRANT_TYPE = "urn:ietf:params:oauth:grant-type:token-exchange"


def get_plugin_config(auth_plugin):
    return auth_plugin.config_class.get_solo()


class TokenAccessAuth(AuthBase):
    def __call__(self, request):
        service = Service.get_service(request.url)
        config = TokenExchangeConfiguration.objects.filter(service=service).first()

        if not config or not storage.plugin:
            return request

        auth_plugin = registry[storage.plugin]
        # Only the plugins that inherit from OIDCAuthentication have the attribute config_class
        if not hasattr(auth_plugin, "config_class"):
            return request

        plugin_config = get_plugin_config(auth_plugin)

        # Perform token exchange
        exchange_url = furl(plugin_config.oidc_op_token_endpoint).set(
            {
                "grant_type": GRANT_TYPE,
                "subject_token": storage.access_token,
                "client_id": plugin_config.oidc_rp_client_id,
                "client_secret": plugin_config.oidc_rp_client_secret,
                "audience": config.audience,
            }
        )

        response = requests.post(
            exchange_url, headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        data = response.json()

        # TODO confirm header name
        request.headers["Authorization"] = data["access_token"]
        return request
