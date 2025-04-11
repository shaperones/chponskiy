"""Configures urls for app's API across all API versions."""

from django.urls import path, include

urlpatterns = [
    path('v1/', include('chponskiy.api.v1.urls')),
]
