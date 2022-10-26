from django.db import models
from django.utils.translation import gettext_lazy as _

import requests
from furl import furl

OPEN_ID_CONFIG_PATH = ".well-known/openid-configuration"


class TokenExchangeConfiguration(models.Model):
    service = models.OneToOneField(
        to="zgw_consumers.Service",
        verbose_name=_("service"),
        help_text=_("External API service"),
        on_delete=models.CASCADE,
    )
    audience = models.CharField(
        verbose_name=_("audience"),
        help_text=_(
            "Specifies the scope/audience, so that Keycloak knows which sort of access token to return."
        ),
        blank=False,
        max_length=250,
    )
    client_id = models.CharField(
        verbose_name=_("client ID"),
        help_text=_("Keycloak client ID."),
        blank=False,
        max_length=250,
    )
    secret = models.CharField(
        verbose_name=_("secret"),
        help_text=_("Keycloak secret for the client ID specified."),
        blank=False,
        max_length=250,
    )
    discovery_endpoint = models.URLField(
        verbose_name=_("discovery endpoint"),
        help_text=_(
            "URL of your OpenID Connect provider discovery endpoint ending with a slash "
            "(`.well-known/...` will be added automatically). "
            "If this is provided, the remaining endpoints can be omitted, as "
            "they will be derived from this endpoint."
        ),
        blank=False,
    )

    class Meta:
        verbose_name = _("Token exchange plugin configuration")

    _token_exchange_endpoint = None

    @property
    def token_exchange_endpoint(self):
        if not self._token_exchange_endpoint:
            discovery_endpoint = furl(self.discovery_endpoint)
            discovery_endpoint /= OPEN_ID_CONFIG_PATH
            response = requests.get(discovery_endpoint.url, timeout=10)
            configuration = response.json()
            self._token_exchange_endpoint = configuration["token_endpoint"]
        return self._token_exchange_endpoint
