from unittest.mock import patch

from django.test import TestCase

from openforms.authentication.constants import FORM_AUTH_SESSION_KEY
from rest_framework.test import APIRequestFactory

from ..signals import clear_storage, extract_access_token

factory = APIRequestFactory()


class SignalReceiverTests(TestCase):
    def test_extract_access_token(self):
        request = factory.get("/foo")
        request.session = {
            FORM_AUTH_SESSION_KEY: {
                "plugin": "plugin1",
                "attribute": "bsn",
                "value": "123",
                "access_token": "some-token",
            }
        }

        with patch(
            "token_exchange.signals.storage", access_token=None, plugin=None
        ) as m_storage:
            extract_access_token(sender="test", request=request)

            self.assertEqual("plugin1", m_storage.plugin)
            self.assertEqual("some-token", m_storage.access_token)

    def test_extract_access_token_no_token(self):
        request = factory.get("/foo")
        request.session = {
            FORM_AUTH_SESSION_KEY: {
                "plugin": "plugin1",
                "attribute": "bsn",
                "value": "123",
            }
        }

        with patch(
            "token_exchange.signals.storage", access_token=None, plugin=None
        ) as m_storage:
            extract_access_token(sender="test", request=request)

            self.assertIsNone(m_storage.plugin)
            self.assertIsNone(m_storage.access_token)

    def test_clear_access_token(self):
        with patch(
            "token_exchange.signals.storage",
            access_token="some-token",
            plugin="plugin1",
        ) as m_storage:
            clear_storage()

            self.assertIsNone(m_storage.plugin)
            self.assertIsNone(m_storage.access_token)
