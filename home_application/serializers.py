from rest_framework import serializers

from .models import Business, Host, Module, Set


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ["biz_name", "biz_id"]


class SetSerializer(serializers.ModelSerializer):
    biz_id = serializers.SerializerMethodField()

    class Meta:
        model = Set
        fields = ["set_name", "set_id", "biz_id"]  # 指定字段列表，与期望输出匹配

    def get_biz_id(self, obj):
        # 返回关联 Business 对象的 biz_id
        return obj.business.biz_id if obj.business else None


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ["module_name", "module_id"]


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        exclude = ["version"]
