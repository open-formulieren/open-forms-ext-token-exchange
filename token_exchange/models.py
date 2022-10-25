from django.db import models
from django.utils.translation import gettext_lazy as _

from zgw_consumers.constants import APITypes


class TokenExchangeConfiguration(models.Model):
    service = models.OneToOneField(
        to="zgw_consumers.Service",
        verbose_name=_("Token exchange service"),
        on_delete=models.PROTECT,
        limit_choices_to={"api_type": APITypes.orc},
        related_name="+",
        null=True,
    )
    audience = models.CharField(
        name="audience",
        verbose_name=_("audience"),
        help_text=_(
            "Specifies the scope/audience, so that Keycloak knows which sort of access token to return."
        ),
        blank=False,
        max_length=250,
    )
    client_id = models.CharField(
        name="client id",
        verbose_name=_("Client ID"),
        help_text=_("Keycloak client ID."),
        blank=False,
        max_length=250,
    )
    secret = models.CharField(
        name="secret",
        verbose_name=_("secret"),
        help_text=_("Keycloak secret for the client ID specified."),
        blank=False,
        max_length=250,
    )
    keycloak_base_url = models.URLField(
        name="keycloak base URL",
        verbose_name=_("keycloak base URL"),
        blank=False,
    )

    class Meta:
        verbose_name = _("Token exchange plugin configuration")
