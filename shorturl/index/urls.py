from django.urls import path

from ..enums import UrlNameEnum
from .views import index

urlpatterns = [
    path(route="", view=index, name=UrlNameEnum.INDEX),
]
