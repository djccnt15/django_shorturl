import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class PayPlan(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Organization(models.Model):
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
    pay_plan = models.ForeignKey(to=PayPlan, on_delete=models.DO_NOTHING, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    full_name = models.CharField(max_length=100, null=True)
    organization = models.ForeignKey(
        to=Organization,
        on_delete=models.DO_NOTHING,
        null=True,
    )


class EmailVerification(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, null=True)
    verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(
        to=Organization,
        on_delete=models.DO_NOTHING,
        null=True,
    )
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ShortenedUrl(models.Model):
    class UrlCreatedVia(models.TextChoices):
        WEBSITE = "web"
        TELEGRAM = "telegram"

    def rand_string():
        str_pool = string.digits + string.ascii_letters
        return "".join([random.choice(seq=str_pool) for _ in range(6)]).lower()

    nick_name = models.CharField(max_length=100)
    category = models.ForeignKey(to=Category, on_delete=models.DO_NOTHING, null=True)
    prefix = models.CharField(max_length=50)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    target_url = models.CharField(max_length=200)
    shortened_url = models.CharField(max_length=6, default=rand_string)
    created_vid = models.CharField(
        max_length=8,
        choices=UrlCreatedVia.choices,
        default=UrlCreatedVia.WEBSITE,
    )
    expired_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
