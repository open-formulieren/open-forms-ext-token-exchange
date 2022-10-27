from typing import TYPE_CHECKING

from django.core.cache import cache
from django.dispatch import receiver

from openforms.submissions.signals import submission_start

if TYPE_CHECKING:
    from openforms.submissions.models import Submission


@receiver(submission_start, dispatch_uid="token_exchange.set_submission_access_token")
def set_submission_access_token(sender, instance: "Submission", request, **kwargs):
    if not hasattr(request, "session"):
        return

    cache.set(
        key=f"accesstoken:{instance.uuid}",
        value=request.session.get("oidc_access_token"),
    )
