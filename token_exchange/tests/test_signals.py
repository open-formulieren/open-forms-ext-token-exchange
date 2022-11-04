from django.core.cache import cache
from django.test import TestCase

from openforms.authentication.constants import FORM_AUTH_SESSION_KEY
from openforms.submissions.tests.factories import SubmissionFactory
from rest_framework.test import APIRequestFactory

from ..signals import set_submission_access_token

factory = APIRequestFactory()


class SignalReceiverTests(TestCase):
    def test_set_accesstoken_in_cache(self):
        request = factory.get("/foo")
        request.session = {
            FORM_AUTH_SESSION_KEY: {
                "plugin": "plugin1",
                "attribute": "bsn",
                "value": "123",
            },
            "oidc_access_token": "test-access-token",
        }
        submission = SubmissionFactory.create()

        set_submission_access_token(sender="test", instance=submission, request=request)

        self.assertEqual(
            cache.get(f"accesstoken:{submission.uuid}"), "test-access-token"
        )

    def test_no_session_on_request(self):
        request = factory.get("/foo")
        submission = SubmissionFactory.build()

        set_submission_access_token(sender="test", instance=submission, request=request)

        self.assertIsNone(cache.get(f"accesstoken:{submission.uuid}"))
