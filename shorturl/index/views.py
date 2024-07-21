from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect

from ..enums import UrlNameEnum


def index(request: WSGIRequest):
    if not request.user.is_authenticated:
        return redirect(to=UrlNameEnum.LOGIN)
    return redirect(to=UrlNameEnum.URL_LIST)
