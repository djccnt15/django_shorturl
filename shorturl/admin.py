from django.contrib import admin

from .models import Organization, PayPlan, Statistic, TrackingParams, User

# Register your models here.


admin.site.register(
    [
        User,
        Organization,
        PayPlan,
        Statistic,
        TrackingParams,
    ]
)
