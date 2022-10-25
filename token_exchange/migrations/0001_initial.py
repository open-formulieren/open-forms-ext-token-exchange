# Generated by Django 3.2.16 on 2022-10-25 15:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("zgw_consumers", "0016_auto_20220818_1412"),
    ]

    operations = [
        migrations.CreateModel(
            name="TokenExchangeConfiguration",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "audience",
                    models.CharField(
                        help_text="Specifies the scope/audience, so that Keycloak knows which sort of access token to return.",
                        max_length=250,
                        verbose_name="audience",
                    ),
                ),
                (
                    "client id",
                    models.CharField(
                        help_text="Keycloak client ID.",
                        max_length=250,
                        verbose_name="Client ID",
                    ),
                ),
                (
                    "secret",
                    models.CharField(
                        help_text="Keycloak secret for the client ID specified.",
                        max_length=250,
                        verbose_name="secret",
                    ),
                ),
                (
                    "keycloak base URL",
                    models.URLField(verbose_name="keycloak base URL"),
                ),
                (
                    "service",
                    models.OneToOneField(
                        limit_choices_to={"api_type": "orc"},
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="zgw_consumers.service",
                        verbose_name="Token exchange service",
                    ),
                ),
            ],
            options={
                "verbose_name": "Token exchange plugin configuration",
            },
        ),
    ]
