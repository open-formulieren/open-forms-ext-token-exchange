from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TokenExchangeConfig(AppConfig):
    name = "token_exchange"
    label = "token_exchange"
    verbose_name = _("Token exchange plugin")

    def ready(self):
        from . import plugin, signals  # noqa
