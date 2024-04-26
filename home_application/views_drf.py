from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import HostFilter, ModuleFilter, SetFilter
from .models import Business, Host, Module, Set
from .serializers import (
    BusinessSerializer,
    HostSerializer,
    ModuleSerializer,
    SetSerializer,
)


class BusinessViewSet(ReadOnlyModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    lookup_field = "biz_id"


class SetViewSet(ReadOnlyModelViewSet):
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    lookup_field = "set_id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = SetFilter


class ModuleViewSet(ReadOnlyModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    lookup_field = "module_id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = ModuleFilter


class CustomPagination(PageNumberPagination):
    page_size = 10  # 默认每页记录数
    page_size_query_param = "limit"  # 允许客户端通过 'limit' 参数改变每页记录数
    max_page_size = 100  # 每页记录数的上限

    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "total_records": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "results": data,
            }
        )


class HostViewSet(ReadOnlyModelViewSet):
    queryset = Host.objects.all().distinct().order_by("host_id")
    serializer_class = HostSerializer
    lookup_field = "host_id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = HostFilter
    pagination_class = CustomPagination  # 使用自定义分页器
