"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path

from shorturl import views as shorturl_view

from .settings import DEBUG

urlpatterns = [
    path(route="admin/", view=admin.site.urls),
    path(route="", view=shorturl_view.index),
    path(route="register", view=shorturl_view.register, name="register"),
]
if DEBUG:
    urlpatterns += [
        # Django Debug Toolbar
        path(route="__debug__/", view=include("debug_toolbar.urls")),
    ]
