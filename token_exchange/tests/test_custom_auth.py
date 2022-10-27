from dataclasses import dataclass
from unittest.mock import patch

from django.test import TestCase

import requests
import requests_mock

from ..auth import TokenAccessAuth
from .factories import TokenExchangeConfigurationFactory


@dataclass
class TestOpenIDConnectPublicConfig:
    oidc_rp_client_id: str
    oidc_rp_client_secret: str
    oidc_op_token_endpoint: str


class CustomAuthClassTests(TestCase):
    def test_no_exchange_token_configuration(self):
        external_api_url = (
            "http://external-api-without-token-exchange.org/user/data/111"
        )

        with requests_mock.mock() as m:
            m.get(external_api_url)

            requests.get(external_api_url, auth=TokenAccessAuth())
            history = m.request_history

        self.assertEqual(1, len(history))
        self.assertNotIn("Authorization", history[0].headers)

    @patch("token_exchange.auth.storage", plugin=None)
    def test_no_plugin_in_storage(self, m_storage):
        external_api_url = (
            "http://external-api-without-token-exchange.org/user/data/111"
        )

        TokenExchangeConfigurationFactory.create(
            service__api_root="http://external-api-with-token-exchange.org/"
        )

        with requests_mock.mock() as m:
            m.get(external_api_url)
            requests.get(external_api_url, auth=TokenAccessAuth())
            history = m.request_history

        self.assertEqual(1, len(history))
        self.assertNotIn("Authorization", history[0].headers)

    @patch(
        "token_exchange.auth.storage",
        access_token="some token to exchange",
        plugin="digid_oidc",
    )
    @patch("token_exchange.auth.get_plugin_config")
    def test_add_header(self, m_config, m_storage):
        external_api_url = "http://external-api-with-token-exchange.org/user/data/111"

        TokenExchangeConfigurationFactory.create(
            service__api_root="http://external-api-with-token-exchange.org/"
        )

        m_config.return_value = TestOpenIDConnectPublicConfig(
            oidc_rp_client_id="digid-client-id",
            oidc_rp_client_secret="digid-secret",
            oidc_op_token_endpoint="http://keycloak.nl/realms/zgw-publiek/protocol/openid-connect/token",
        )
        with requests_mock.mock() as m:
            m.get(external_api_url)
            m.post(
                "http://keycloak.nl/realms/zgw-publiek/protocol/openid-connect/token",
                json={"access_token": "wonderful-token"},
            )

            requests.get(external_api_url, auth=TokenAccessAuth())
            history = m.request_history

        self.assertEqual(2, len(history))
        self.assertIn("Authorization", history[1].headers)
