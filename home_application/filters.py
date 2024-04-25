import django_filters

from .models import Host, Module, Set


# filter
class SetFilter(django_filters.FilterSet):
    business = django_filters.NumberFilter(field_name="business__biz_id")

    class Meta:
        model = Set
        fields = ["business"]


class ModuleFilter(django_filters.FilterSet):
    business = django_filters.NumberFilter(field_name="set__business__biz_id")
    set = django_filters.NumberFilter(field_name="set__set_id")

    class Meta:
        model = Module
        fields = ["set", "business"]


class HostFilter(django_filters.FilterSet):
    business = django_filters.NumberFilter(method="filter_by_business")
    set = django_filters.NumberFilter(method="filter_by_set")
    module = django_filters.NumberFilter(method="filter_by_module")
    operator = django_filters.CharFilter(field_name="operator", lookup_expr="icontains")
    bak_operator = django_filters.CharFilter(field_name="bak_operator", lookup_expr="icontains")
    host_innerip = django_filters.CharFilter(field_name="host_innerip", lookup_expr="icontains")
    host_outerip = django_filters.CharFilter(field_name="host_outerip", lookup_expr="icontains")
    cloud_vendor = django_filters.CharFilter(field_name="cloud_vendor", lookup_expr="icontains")

    class Meta:
        model = Host
        fields = ["operator", "bak_operator", "host_innerip", "host_outerip", "cloud_vendor"]

    def filter_by_business(self, queryset, name, value):
        return queryset.filter(modules__set__business__biz_id=value)

    def filter_by_set(self, queryset, name, value):
        return queryset.filter(modules__set__set_id=value)

    def filter_by_module(self, queryset, name, value):
        return queryset.filter(modules__module_id=value)
