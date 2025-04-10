"""
URL configuration for django_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.views import serve as static_serve
from functools import partial

from chponskiy.views import index, auth, register, profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login', auth, name='login'),
    path('register', register, name='register'),
    path('profile', profile, name='profile'),
    path('favicon.ico', partial(static_serve, path='img/favicon.ico'), name='favicon'),
]

if DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns.extend(debug_toolbar_urls())
