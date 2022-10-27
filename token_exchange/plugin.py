import logging

from openforms.pre_requests.base import PreRequestHookBase
from openforms.pre_requests.registry import register

from .auth import TokenAccessAuth

logger = logging.getLogger(__name__)


@register("token_exchange")
class TokenExchangePreRequestHook(PreRequestHookBase):
    def __call__(self, method: str, url: str, **kwargs):
        if kwargs["auth"]:
            logger.warning(
                "Overwriting existing authentication with custom authentication class."
            )
        kwargs["auth"] = TokenAccessAuth()
