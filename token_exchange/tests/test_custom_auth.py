from unittest.mock import patch

from django.test import TestCase

import requests
import requests_mock

from ..auth import TokenAccessAuth
from .factories import TokenExchangeConfigurationFactory


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
        self.assertNotIn("haal-centraal-header-TODO", history[0].headers)

    def test_add_header(self):
        external_api_url = "http://external-api-with-token-exchange.org/user/data/111"

        TokenExchangeConfigurationFactory.create(
            service__api_root="http://external-api-with-token-exchange.org/"
        )

        with requests_mock.mock() as m:
            m.get(external_api_url)
            m.get(
                "http://keycloak.nl/realms/zgw-publiek/.well-known/openid-configuration",
                json={
                    "token_endpoint": "http://keycloak.nl/realms/zgw-publiek/protocol/openid-connect/token"
                },
            )
            m.post(
                "http://keycloak.nl/realms/zgw-publiek/protocol/openid-connect/token",
                json={"access_token": "wonderful-token"},
            )

            with patch("token_exchange.auth.storage") as m_storage:

                class TestStorage:
                    """Mock the thread local storage for the Keycloak token"""

                    access_token = "some token to exchange"

                m_storage.return_value = TestStorage()
                requests.get(external_api_url, auth=TokenAccessAuth())
                history = m.request_history

        self.assertEqual(3, len(history))
        self.assertIn("haal-centraal-header-TODO", history[2].headers)
