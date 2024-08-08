from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.aggregates import Count

# from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django_ratelimit.decorators import ratelimit

from ..enums import UrlNameEnum
from ..models import ShortenedUrl, Statistic
from ..utils import get_kst
from .forms import UrlCreateForm


@ratelimit(key="ip", rate="3/m")
def url_redirect(request: WSGIRequest, prefix, url):
    was_limited = getattr(request, "limited", False)
    if was_limited:
        return redirect(to=UrlNameEnum.INDEX)
    get_url = get_object_or_404(klass=ShortenedUrl, prefix=prefix, shortened_url=url)
    is_permanent = False
    target = get_url.target_url
    if get_url.creator.organization:
        is_permanent = True

    if not target.startswith("https://") and not target.startswith("http://"):
        target = "https://" + get_url.target_url

    custom_params = request.GET.dict() if request.GET.dict() else None
    history = Statistic()
    history.record(request=request, url=get_url, params=custom_params)
    return redirect(to=target, permanent=is_permanent)


def url_list(request: WSGIRequest):
    if not request.user.is_authenticated:
        return redirect(to=UrlNameEnum.LOGIN)

    # statics = (
    #     Statistic.objects.filter(shortened_url_id=5)
    #     .values("custom_params__email_id")
    #     .annotate(t=Count("custom_params__email_id"))
    # )
    # print(statics)

    return render(request=request, template_name="url_list.html")


@login_required
def url_create(request: WSGIRequest):
    msg = None
    if request.method == "POST":
        form = UrlCreateForm(request.POST)
        if form.is_valid():
            msg = f"{form.cleaned_data.get('nick_name')} 생성 완료!"
            messages.add_message(request, messages.INFO, msg)
            form.save(request)
            return redirect(to=UrlNameEnum.URL_LIST)
        else:
            form = UrlCreateForm()
    else:
        form = UrlCreateForm()
    return render(
        request=request,
        template_name="url_create.html",
        context={"form": form},
    )


@login_required
def url_change(request: WSGIRequest, action, url_id):
    if request.method == "POST":
        url_data = ShortenedUrl.objects.filter(id=url_id)
        if url_data.exists():
            if url_data.first().creator != request.user.id:
                msg = "자신이 소유하지 않은 URL 입니다."
            else:
                if action == "delete":
                    msg = f"{url_data.first().nick_name} 삭제 완료!"
                    url_data.delete()
                    messages.add_message(request, messages.INFO, msg)
                elif action == "update":
                    msg = f"{url_data.first().nick_name} 수정 완료!"
                    form = UrlCreateForm(request.POST)
                    form.update_form(request, url_id)

                    messages.add_message(request, messages.INFO, msg)
        else:
            msg = "해당 URL 정보를 찾을 수 없습니다."

    elif request.method == "GET" and action == "update":
        url_data = ShortenedUrl.objects.filter(pk=url_id).first()
        form = UrlCreateForm(instance=url_data)
        return render(
            request=request,
            template_name="url_create.html",
            context={"form": form, "is_update": True},
        )

    return redirect(to=UrlNameEnum.URL_LIST)


@cache_page(timeout=10)
def statistic_view(request, url_id: int):
    url_info = get_object_or_404(ShortenedUrl, pk=url_id)
    base_qs = Statistic.objects.filter(
        shortened_url_id=url_id, created_at__gte=get_kst() - timedelta(days=14)
    )
    clicks = (
        base_qs.values("created_at__date")
        .annotate(clicks=Count("id"))
        .values("created_at__date", "clicks")
        .order_by("created_at__date")
    )

    date_list = [c.get("created_at__date").strftime("%Y-%m-%d") for c in clicks]
    click_list = [c.get("clicks") for c in clicks]
    return render(
        request=request,
        template_name="statistics.html",
        context={
            "url": url_info,
            "kst": get_kst(),
            "date_list": date_list,
            "click_list": click_list,
        },
    )
