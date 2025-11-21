from django.core.cache import cache
from django.test import TestCase

import requests
import requests_mock
from mozilla_django_oidc_db.models import OIDCClient
from mozilla_django_oidc_db.tests.factories import (
    OIDCProviderFactory,
)

from openforms.authentication.registry import register as auth_register
from openforms.submissions.tests.factories import SubmissionFactory

from ..auth import TokenAccessAuth
from .factories import TokenExchangeConfigurationFactory


class CustomAuthClassTests(TestCase):
    def test_no_exchange_token_configuration(self):
        external_api_url = (
            "http://external-api-without-token-exchange.org/user/data/111"
        )
        submission = SubmissionFactory.create()

        with requests_mock.mock() as m:
            m.get(external_api_url)

            requests.get(external_api_url, auth=TokenAccessAuth(submission))
            history = m.request_history

        self.assertEqual(1, len(history))
        self.assertNotIn("Authorization", history[0].headers)

    def test_no_authenticated_submission(self):
        external_api_url = (
            "http://external-api-without-token-exchange.org/user/data/111"
        )

        TokenExchangeConfigurationFactory.create(
            service__api_root="http://external-api-with-token-exchange.org/"
        )
        submission = SubmissionFactory.create()

        with requests_mock.mock() as m:
            m.get(external_api_url)
            requests.get(external_api_url, auth=TokenAccessAuth(submission))
            history = m.request_history

        self.assertEqual(1, len(history))
        self.assertNotIn("Authorization", history[0].headers)

    def test_no_access_token_in_cache(self):
        external_api_url = (
            "http://external-api-without-token-exchange.org/user/data/111"
        )

        TokenExchangeConfigurationFactory.create(
            service__api_root="http://external-api-with-token-exchange.org/"
        )
        submission = SubmissionFactory.create(auth_info__plugin="digid_oidc")

        with requests_mock.mock() as m:
            m.get(external_api_url)
            requests.get(external_api_url, auth=TokenAccessAuth(submission))
            history = m.request_history

        self.assertEqual(1, len(history))
        self.assertNotIn("Authorization", history[0].headers)

    def test_add_header(self):
        auth_plugin = auth_register["digid_oidc"]
        client = OIDCClient.objects.get(identifier=auth_plugin.oidc_plugin_identifier)
        client.oidc_provider = OIDCProviderFactory.create(
            oidc_op_token_endpoint="http://keycloak.nl/realms/zgw-publiek/protocol/openid-connect/token"
        )
        client.oidc_rp_client_id = "digid-client-id"
        client.oidc_rp_client_secret = "digid-secret"
        client.save()
        external_api_url = "http://external-api-with-token-exchange.org/user/data/111"

        TokenExchangeConfigurationFactory.create(
            service__api_root="http://external-api-with-token-exchange.org/"
        )
        submission = SubmissionFactory.create(auth_info__plugin=auth_plugin.identifier)
        cache.set(f"accesstoken:{submission.uuid}", submission)
        with requests_mock.mock() as m:
            m.get(external_api_url)
            m.post(
                "http://keycloak.nl/realms/zgw-publiek/protocol/openid-connect/token",
                json={"access_token": "wonderful-token"},
            )

            requests.get(external_api_url, auth=TokenAccessAuth(submission))
            history = m.request_history

        # One call to the token exchange endpoint, one call to the external API
        self.assertEqual(2, len(history))
        self.assertIn("Authorization", history[1].headers)
