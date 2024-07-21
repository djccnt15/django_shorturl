from django.urls import path

from ..enums import UrlNameEnum
from . import views

urlpatterns = [
    path(route=UrlNameEnum.REGISTER, view=views.register, name=UrlNameEnum.REGISTER),
    path(route=UrlNameEnum.LOGIN, view=views.login_view, name=UrlNameEnum.LOGIN),
    path(route=UrlNameEnum.LOGOUT, view=views.logout_view, name=UrlNameEnum.LOGOUT),
]
