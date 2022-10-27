import threading

from django.core import signals
from django.dispatch import receiver

from openforms.authentication.constants import FORM_AUTH_SESSION_KEY
from openforms.authentication.signals import authentication_success

storage = threading.local()


@receiver(authentication_success, dispatch_uid="token_exchange.extract_access_token")
def extract_access_token(sender, request, **kwargs) -> None:
    if not hasattr(request, "session"):
        return

    form_auth = request.session[FORM_AUTH_SESSION_KEY]
    if not (access_token := form_auth.get("access_token")):
        return

    storage.access_token = access_token
    storage.plugin = form_auth["plugin"]


def clear_storage(**kwargs):
    storage.access_token = None
    storage.plugin = None


signals.request_finished.connect(clear_storage)
