from django import forms
from django.core.handlers.wsgi import WSGIRequest

from shorturl.models import ShortenedUrl
from shorturl.utils import url_count_changer


class UrlCreateForm(forms.ModelForm):
    class Meta:
        model = ShortenedUrl
        fields = ["nick_name", "target_url"]
        labels = {
            "nick_name": ("별칭"),
            "target_url": ("URL"),
        }
        widgets = {
            "nick_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "URL을 구분하기 위한 별칭",
                }
            ),
            "target_url": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "포워딩될 URL",
                }
            ),
        }

    def save(self, request: WSGIRequest, commit=True, is_admin=False):
        instance: ShortenedUrl = super(UrlCreateForm, self).save(commit=False)
        if not is_admin:
            instance.creator = request.user
        instance.target_url = instance.target_url.strip()
        if commit:
            try:
                instance.save()
            except Exception as e:
                print(e)
            else:
                url_count_changer(request, True)
        return instance

    def update_form(self, request: WSGIRequest, url_id, is_admin=False):
        instance: ShortenedUrl = super(UrlCreateForm, self).save(commit=False)
        instance.target_url = instance.target_url.strip()
        ShortenedUrl.objects.filter(pk=url_id).update(
            target_url=instance.target_url,
            nick_name=instance.nick_name,
        )
