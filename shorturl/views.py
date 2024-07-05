from django.contrib.auth import authenticate, login
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render

from .forms import RegisterForm

# Create your views here.


def index(request: WSGIRequest):
    # temporal redirect to admin page
    return redirect(to="admin/")


def register(request: WSGIRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        msg = "올바르지 않은 데이터 입니다."
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request=request, user=user)
            msg = "회원가입완료"
        return render(
            request=request,
            template_name="register.html",
            context={"form": form, "msg": msg},
        )
    else:
        form = RegisterForm()
    return render(
        request=request,
        template_name="register.html",
        context={"form": form},
    )
