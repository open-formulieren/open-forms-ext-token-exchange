from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import TokenExchangeConfiguration


@admin.register(TokenExchangeConfiguration)
class TokenExchangeConfigurationAdmin(ModelAdmin):
    pass
