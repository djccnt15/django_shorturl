from django.core.handlers.wsgi import WSGIRequest
from django.db.models import F

from .models import User


def url_count_changer(request: WSGIRequest, is_increase: bool):
    count_number = 1 if is_increase else -1
    User.objects.filter(id=request.user.id).update(
        url_count=F("url_count") + count_number
    )
