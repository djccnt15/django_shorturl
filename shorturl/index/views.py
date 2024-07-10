from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect


def index(request: WSGIRequest):
    if not request.user.is_authenticated:
        return redirect(to="login")
    return redirect(to="urls/")
