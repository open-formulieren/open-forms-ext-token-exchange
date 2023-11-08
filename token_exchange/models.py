from django.db import models
from django.utils.translation import gettext_lazy as _


class TokenExchangeConfiguration(models.Model):
    label = models.CharField(
        verbose_name=_("label"),
        help_text=_("The label of this token exchange configuration"),
        max_length=250,
        blank=True,
    )
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

    class Meta:
        verbose_name = _("Token exchange plugin configuration")

    def save(self, *args, **kwargs) -> None:
        if not self.label and (self.service and self.service.label):
            self.label = self.service.label
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        if not self.label:
            return super().__str__()

        return self.label
