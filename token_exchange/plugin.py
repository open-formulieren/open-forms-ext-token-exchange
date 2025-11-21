import logging

from openforms.pre_requests.base import PreRequestHookBase
from openforms.pre_requests.clients import PreRequestClientContext
from openforms.pre_requests.registry import register

from .auth import TokenAccessAuth

logger = logging.getLogger(__name__)


@register("token_exchange")
class TokenExchangePreRequestHook(PreRequestHookBase):
    def __call__(
        self,
        method: str,
        url: str,
        kwargs,
        context: PreRequestClientContext | None = None,
    ):
        if "auth" in kwargs:
            logger.warning(
                "Overwriting existing authentication with custom authentication class."
            )

        if context and "submission" in context:
            kwargs["auth"] = TokenAccessAuth(submission=context["submission"])
