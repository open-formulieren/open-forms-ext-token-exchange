# Generated by Django 3.2.16 on 2022-10-27 09:47

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
                    "service",
                    models.OneToOneField(
                        help_text="External API service",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="zgw_consumers.service",
                        verbose_name="service",
                    ),
                ),
            ],
            options={
                "verbose_name": "Token exchange plugin configuration",
            },
        ),
    ]
