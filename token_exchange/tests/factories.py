import factory
from zgw_consumers.models import Service

from ..models import TokenExchangeConfiguration


class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Service


class TokenExchangeConfigurationFactory(factory.django.DjangoModelFactory):
    service = factory.SubFactory(ServiceFactory)
    audience = "target-client"

    class Meta:
        model = TokenExchangeConfiguration
