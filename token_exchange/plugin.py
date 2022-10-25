from openforms.pre_requests.base import PreRequestHookBase
from openforms.pre_requests.registry import register

from .auth import TokenAccessAuth


@register("token_exchange")
class TokenExchangePreRequestHook(PreRequestHookBase):
    def __call__(self, method: str, url: str, **kwargs):
        kwargs["auth"] = TokenAccessAuth
