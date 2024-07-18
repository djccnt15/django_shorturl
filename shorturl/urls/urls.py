from django.urls import path
from rest_framework import routers

from . import views
from .apis import UrlListView

router = routers.DefaultRouter()
router.register(prefix=r"urls", viewset=UrlListView)

urlpatterns = [
    path(route="", view=views.url_list, name="url_list"),
    path(route="create", view=views.url_create, name="url_create"),
    path(route="<str:action>/<int:url_id>", view=views.url_change, name="url_change"),
]
