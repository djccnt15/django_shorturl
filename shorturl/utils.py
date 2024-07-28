from datetime import datetime, timedelta, timezone

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import F
from rest_framework.request import Request
from rest_framework.response import Response

from .models import User


def url_count_changer(request: WSGIRequest | Request, is_increase: bool):
    count_number = 1 if is_increase else -1
    User.objects.filter(id=request.user.id).update(
        url_count=F("url_count") + count_number
    )


def MsgOk(status: int = 200):
    return Response({"msg": "ok"}, status=status)


def get_kst():
    KST = timezone(offset=timedelta(hours=9), name="KST")
    return datetime.now(tz=KST)
