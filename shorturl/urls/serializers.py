from rest_framework import serializers
from rest_framework.request import Request

from ..models import ShortenedUrl, User
from ..utils import url_count_changer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class UrlListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedUrl
        fields = "__all__"
        # fields = [
        #     "id",
        #     "nick_name",
        #     "prefix",
        #     "shortened_url",
        #     "creator",
        #     "click",
        #     "created_via",
        #     "expired_at",
        # ]

    creator = UserSerializer(read_only=True)


class UrlCreateSerializer(serializers.Serializer):
    nick_name = serializers.CharField(max_length=50)
    target_url = serializers.CharField(max_length=2000)
    category = serializers.IntegerField(required=False)

    def create(self, request: Request, data, commit=True):
        instance = ShortenedUrl()
        instance.creator_id = request.user.id
        instance.category = data.get("category", None)
        instance.target_url = data.get("target_url").strip()
        if commit:
            try:
                instance.save()
            except Exception as e:
                print(e)
            else:
                url_count_changer(request, True)
        return instance
