from dataclasses import dataclass

from django.core.cache import cache

import requests
from mozilla_django_oidc_db.registry import register as oidc_registry
from requests.auth import AuthBase
from zgw_consumers.models import Service

from openforms.authentication.registry import register as registry
from openforms.contrib.auth_oidc.plugin import OIDCAuthentication
from openforms.submissions.models import Submission

from .models import TokenExchangeConfiguration

# Docs https://www.keycloak.org/docs/latest/securing_apps/#_token-exchange
GRANT_TYPE = "urn:ietf:params:oauth:grant-type:token-exchange"


@dataclass
class OIDCConfig:
    oidc_rp_client_id: str
    oidc_rp_client_secret: str
    oidc_op_token_endpoint: str


def get_plugin_config(auth_plugin: OIDCAuthentication) -> OIDCConfig:
    oidc_plugin = oidc_registry[auth_plugin.oidc_plugin_identifier]
    client_config = oidc_plugin.get_config()
    assert client_config.oidc_provider is not None
    return OIDCConfig(
        oidc_rp_client_id=client_config.oidc_rp_client_id,
        oidc_rp_client_secret=client_config.oidc_rp_client_secret,
        oidc_op_token_endpoint=client_config.oidc_provider.oidc_op_token_endpoint,
    )


@dataclass
class TokenAccessAuth(AuthBase):
    submission: Submission

    def __call__(self, request):
        service = Service.get_service(request.url)
        config = TokenExchangeConfiguration.objects.filter(service=service).first()

        if not config or not self.submission or not self.submission.is_authenticated:
            return request

        access_token = cache.get(f"accesstoken:{self.submission.uuid}")

        if not access_token:
            return request

        auth_plugin = registry[self.submission.auth_info.plugin]

        # Only the plugins that inherit from OIDCAuthentication have OIDC configuration.
        if not isinstance(auth_plugin, OIDCAuthentication):
            return request

        plugin_config = get_plugin_config(auth_plugin)
        # Perform token exchange
        response = requests.post(
            plugin_config.oidc_op_token_endpoint,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": GRANT_TYPE,
                "subject_token": access_token,
                "client_id": plugin_config.oidc_rp_client_id,
                "client_secret": plugin_config.oidc_rp_client_secret,
                "audience": config.audience,
            },
        )
        response.raise_for_status()
        data = response.json()

        request.headers["Authorization"] = data["access_token"]
        return request
