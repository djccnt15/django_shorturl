from django.http.response import Http404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from ..models import ShortenedUrl
from ..utils import MsgOk, url_count_changer
from .serializers import UrlCreateSerializer, UrlListSerializer


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
        url_count_changer(request, False)
        return MsgOk()

    # GET ALL
    def list(self, request):
        queryset = self.get_queryset().all()
        serializer = UrlListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get", "post"])
    def add_click(self, request: Request, pk=None):
        queryset = self.get_queryset().filter(pk=pk, creator_id=request.user.id)
        if not queryset.exists():
            raise Http404
        rtn = queryset.first().clicked()
        serializer = UrlListSerializer(rtn)
        return Response(serializer.data)
