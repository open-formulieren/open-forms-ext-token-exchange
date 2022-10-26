import factory
from zgw_consumers.models import Service

from ..models import TokenExchangeConfiguration


class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Service


class TokenExchangeConfigurationFactory(factory.django.DjangoModelFactory):
    service = factory.SubFactory(ServiceFactory)
    audience = "target-client"
    client_id = "starting-client"
    secret = "the client secret"
    discovery_endpoint = "http://keycloak.nl/realms/zgw-publiek/"

    class Meta:
        model = TokenExchangeConfiguration
