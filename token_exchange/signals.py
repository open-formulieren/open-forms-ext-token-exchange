import threading

from django.core import signals
from django.dispatch import receiver

from openforms.authentication.signals import authentication_success

storage = threading.local()


@receiver(authentication_success, dispatch_uid="token_exchange.extract_access_token")
def extract_access_token(sender, request, **kwargs) -> None:
    # TODO Extract token from request
    access_token = "some extracted token"
    id_token = "some extracted id token"

    storage.access_token = access_token
    storage.id_token = id_token  # TODO not sure if needed yet


def clear_tokens(**kwargs):
    storage.access_token = None
    storage.id_token = None


signals.request_finished.connect(clear_tokens)
