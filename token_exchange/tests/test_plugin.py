from django.test import TestCase

from openforms.pre_requests.clients import PreRequestClientContext
from openforms.submissions.tests.factories import SubmissionFactory

from ..plugin import TokenExchangePreRequestHook


class TestPlugin(TestCase):
    def test_kwargs_updated(self):
        kwargs = {}
        hook = TokenExchangePreRequestHook(identifier="test")
        contex = PreRequestClientContext(submission=SubmissionFactory.build())
        hook(url="http://test.nl/", method="POST", kwargs=kwargs, context=contex)

        self.assertIn("auth", kwargs)
