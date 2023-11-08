from django.test import TestCase

from .factories import TokenExchangeConfigurationFactory


class TokenExchangeConfigurationTests(TestCase):
    def test_string_method_with_service_label(self):
        config = TokenExchangeConfigurationFactory.create(service__label="A label")

        self.assertEqual("A label", str(config))

    def test_string_method_withou_service_label(self):
        config = TokenExchangeConfigurationFactory.create()

        self.assertEqual(
            f"TokenExchangeConfiguration object ({config.pk})", str(config)
        )

    def test_save_does_not_overwrite_label(self):
        config = TokenExchangeConfigurationFactory.create(
            label="A config label", service__label="A service label"
        )

        self.assertEqual("A config label", str(config))
