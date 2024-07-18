import random
import string

from django.contrib.auth.models import AbstractUser
from django.core.handlers.wsgi import WSGIRequest
from django.db import models

from . import model_utils

# Create your models here.


class TimeStampModel(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PayPlan(TimeStampModel):
    name = models.CharField(max_length=20)
    price = models.IntegerField()


class Organization(TimeStampModel):
    class Industries(models.TextChoices):
        PERSONAL = "personal"
        RETAIL = "retail"
        MANUFACTURING = "manufacturing"
        IT = "it"
        OTHERS = "others"

    name = models.CharField(max_length=50)
    industry = models.CharField(
        max_length=15,
        choices=Industries.choices,
        default=Industries.OTHERS,
    )
    pay_plan = models.ForeignKey(
        to=PayPlan,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )


class User(AbstractUser):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    telegram_username = models.CharField(max_length=100, null=True, blank=True)
    url_count = models.IntegerField(default=0)
    organization = models.ForeignKey(
        to=Organization,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )


class EmailVerification(TimeStampModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, null=True, blank=True)
    verified = models.BooleanField(default=False)


class Category(TimeStampModel):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(
        to=Organization,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)


class ShortenedUrl(TimeStampModel):
    class Meta:
        indexes = [models.Index(fields=["prefix", "shortened_url"])]

    class UrlCreatedVia(models.TextChoices):
        WEBSITE = "web"
        TELEGRAM = "telegram"

    def rand_string():
        str_pool = string.digits + string.ascii_letters
        return "".join([random.choice(seq=str_pool) for _ in range(6)]).lower()

    def rand_letter():
        str_pool = string.ascii_letters
        return random.choice(str_pool).lower()

    nick_name = models.CharField(max_length=100)
    category = models.ForeignKey(
        to=Category,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    prefix = models.CharField(max_length=50, default=rand_letter)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    target_url = models.CharField(max_length=200)
    shortened_url = models.CharField(max_length=6, default=rand_string)
    created_via = models.CharField(
        max_length=8,
        choices=UrlCreatedVia.choices,
        default=UrlCreatedVia.WEBSITE,
    )
    expired_at = models.DateTimeField(null=True, blank=True)
    click = models.BigIntegerField(default=0)

    def clicked(self):
        self.click += 1
        self.save()
        return self


class Statistic(TimeStampModel):
    class ApproachDevice(models.TextChoices):
        PC = "pc"
        MOBILE = "mobile"
        TABLET = "tablet"

    shortened_url = models.ForeignKey(ShortenedUrl, on_delete=models.CASCADE)
    ip = models.CharField(max_length=15)
    web_browser = models.CharField(max_length=50)
    device = models.CharField(max_length=6, choices=ApproachDevice.choices)
    device_os = models.CharField(max_length=30)
    country_code = models.CharField(max_length=2, default="XX")
    country_name = models.CharField(max_length=100, default="UNKNOWN")
    custom_params = models.JSONField(null=True)

    def record(self, *, request: WSGIRequest, url: ShortenedUrl, params: dict):
        self.shortened_url = url

        # TODO this will catch web server IP on product env
        self.ip = request.META["REMOTE_ADDR"]

        self.web_browser = request.user_agent.browser.family
        self.device = (
            self.ApproachDevice.MOBILE
            if request.user_agent.is_mobile
            else (
                self.ApproachDevice.TABLET
                if request.user_agent.is_tablet
                else self.ApproachDevice.PC
            )
        )
        self.device_os = request.user_agent.os.family
        if params:
            tracking_param = TrackingParams.get_tracking_params(url.id)
            self.custom_params = model_utils.dict_slice(
                d=model_utils.dict_filter(
                    d=params,
                    filter_list=tracking_param,
                ),
                n=5,
            )

        try:
            country = model_utils.location_finder(request=request)
            self.country_code = country.get("country_code", "XX")
            self.country_name = country.get("country_name", "UNKNOWN")
        except Exception:
            pass
        url.clicked()
        self.save()


class TrackingParams(TimeStampModel):
    shortened_url = models.ForeignKey(ShortenedUrl, on_delete=models.CASCADE)
    params = models.CharField(max_length=20)

    @classmethod
    def get_tracking_params(cls, shortened_url_id: int):
        return cls.objects.filter(shortened_url_id=shortened_url_id).values_list(
            "params", flat=True
        )
