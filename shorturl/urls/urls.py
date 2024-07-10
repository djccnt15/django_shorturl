from django.urls import path

from . import views

urlpatterns = [
    path(route="", view=views.url_list, name="url_list"),
    path(route="create", view=views.url_create, name="url_create"),
    path(route="<str:action>/<int:url_id>", view=views.url_change, name="url_change"),
]
