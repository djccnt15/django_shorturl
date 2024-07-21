from django.contrib.auth import authenticate, login, logout
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render

from ..enums import UrlNameEnum
from ..models import User
from .forms import LoginForm, RegisterForm

# Create your views here.


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


def login_view(request: WSGIRequest):
    is_ok = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email: str = form.cleaned_data.get("email", "")
            raw_password: str = form.cleaned_data.get("password", "")
            remember_me: bool = form.cleaned_data.get("remember_me", False)
            msg = "올바른 유저ID와 패스워드를 입력하세요."
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            else:
                if user.check_password(raw_password):
                    msg = None
                    login(request=request, user=user)
                    is_ok = True
                    request.session["remember_me"] = remember_me
                    if not remember_me:
                        request.session.set_expiry(value=0)
    else:
        msg = None
        form = LoginForm()
    # print("REMEMBER_ME: ", request.session.get("remember_me"))
    if request.user.is_authenticated:
        return redirect(to=UrlNameEnum.URL_LIST)
    return render(
        request=request,
        template_name="login.html",
        context={"form": form, "msg": msg, "is_ok": is_ok},
    )


def logout_view(request: WSGIRequest):
    logout(request=request)
    return redirect(to=UrlNameEnum.LOGIN)
