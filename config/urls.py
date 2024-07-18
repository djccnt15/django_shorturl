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

from shorturl.index import urls as index_url
from shorturl.urls import urls as url_url
from shorturl.urls import views as url_view
from shorturl.user import urls as user_url

from .settings import DEBUG

urlpatterns = [
    path(route="admin/", view=admin.site.urls),
    path(route="", view=include(index_url.urlpatterns)),
    path(route="", view=include(user_url.urlpatterns)),
    path(route="urls/", view=include(url_url.urlpatterns)),
    path(route="api/", view=include(url_url.router.urls)),
    path(route="<str:prefix>/<str:url>", view=url_view.url_redirect),
]
if DEBUG:
    urlpatterns += [
        # Django Debug Toolbar
        path(route="__debug__/", view=include("debug_toolbar.urls")),
    ]
