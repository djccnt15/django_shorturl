from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect

# Create your views here.


def index(request: WSGIRequest):
    # temporal redirect to admin page
    return redirect(to="admin/")
