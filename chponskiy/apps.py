"""Configures Django apps to be included in this project"""

from django.apps import AppConfig


class ChponskiyConfig(AppConfig):
    """Django app configuration"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chponskiy'
