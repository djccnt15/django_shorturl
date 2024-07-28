from datetime import timedelta

from django.db.models.aggregates import Count
from django.http.response import Http404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from .. import utils
from ..models import ShortenedUrl, Statistic
from .serializers import BrowerStatSerializer, UrlCreateSerializer, UrlListSerializer


class UrlListView(viewsets.ModelViewSet):
    queryset = ShortenedUrl.objects.order_by("-created_at")
    serializer_class = UrlListSerializer
    permission_classes = [permissions.IsAuthenticated]

    # POST METHOD
    def create(self, request: Request):
        serializer = UrlCreateSerializer(data=request.data)
        if serializer.is_valid():
            rtn = serializer.create(request=request, data=serializer.data)
            return Response(UrlListSerializer(rtn).data, status=status.HTTP_201_CREATED)
        pass

    # Detail GET
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk).first()
        serializer = UrlListSerializer(queryset)
        return Response(serializer.data)

    # TODO PUT METHOD
    def update(self, request, pk=None):
        pass

    # TODO PATCH METHOD
    def partial_update(self, request, pk=None):
        pass

    # DELETE METHOD
    @renderer_classes([JSONRenderer])
    def destroy(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk, creator_id=request.user.id)
        if not queryset.exists():
            raise Http404
        queryset.delete()
        utils.url_count_changer(request, False)
        return utils.MsgOk()

    # GET ALL
    def list(self, request):
        queryset = self.get_queryset().all()
        serializer = UrlListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get", "post"])
    def add_browser_today(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk, creator_id=request.user.id).first()
        new_history = Statistic()
        new_history.record(request=request, url=queryset, params={})
        return utils.MsgOk()

    @action(detail=True, methods=["get"])
    def get_browser_stats(self, request, pk=None):
        queryset = Statistic.objects.filter(
            shortened_url_id=pk,
            shortened_url__creator_id=request.user.id,
            created_at__gte=utils.get_kst() - timedelta(days=14),
        )
        if not queryset.exists():
            raise Http404
        # browers = (
        #     queryset.values("web_browser", "created_at__date")
        #     .annotate(count=Count("id"))
        #     .values("count", "web_browser", "created_at__date")
        #     .order_by("-created_at__date")
        # )
        browers = (
            queryset.values("web_browser")
            .annotate(count=Count("id"))
            .values("count", "web_browser")
            .order_by("-count")
        )
        serializer = BrowerStatSerializer(browers, many=True)
        return Response(serializer.data)
