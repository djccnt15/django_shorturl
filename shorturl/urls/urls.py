from django.urls import path
from rest_framework import routers

from ..enums import UrlNameEnum
from . import views
from .apis import UrlListView

router = routers.DefaultRouter()
router.register(prefix=r"urls", viewset=UrlListView)

urlpatterns = [
    path(route="", view=views.url_list, name=UrlNameEnum.URL_LIST),
    path(route="create", view=views.url_create, name=UrlNameEnum.URL_CREATE),
    path(
        route="<str:action>/<int:url_id>",
        view=views.url_change,
        name=UrlNameEnum.URL_CHANGE,
    ),
    path(
        route="<int:url_id>/statistic",
        view=views.statistic_view,
        name="statistic_view",
    ),
]
