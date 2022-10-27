from dataclasses import dataclass

from django.core.cache import cache

import requests
from openforms.authentication.registry import register as registry
from openforms.submissions.models import Submission
from requests.auth import AuthBase
from zgw_consumers.models import Service

from .models import TokenExchangeConfiguration

# Docs https://www.keycloak.org/docs/latest/securing_apps/#_token-exchange
GRANT_TYPE = "urn:ietf:params:oauth:grant-type:token-exchange"


def get_plugin_config(auth_plugin):
    return auth_plugin.config_class.get_solo()


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
        # Only the plugins that inherit from OIDCAuthentication have the attribute config_class
        if not hasattr(auth_plugin, "config_class"):
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
