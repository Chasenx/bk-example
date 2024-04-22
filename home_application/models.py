"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from enum import Enum

import django.utils.timezone as timezone
from django.db import models


class Backup(models.Model):
    host_ip = models.CharField("备份主机IP", max_length=100, default="")
    dir = models.CharField("备份目录", max_length=100, default="")
    suffix = models.CharField("备份名后缀", max_length=100, default="")
    backup_user = models.CharField("备份人", max_length=100, default="")
    backup_time = models.DateTimeField("备份时间", default=timezone.now)
    backup_files = models.CharField("备份文件名", max_length=100, default="")
    job_link = models.CharField("JOB链接", max_length=100, default="")
    job_instance_id = models.CharField("job_instance_id", max_length=100, default="")


class Version(models.Model):
    class StatusEnum(Enum):
        NOT_STARTED = "Not Started"
        SYNCING = "Syncing"
        FAIL = "Fail"
        SUCCESS = "Success"

    sync_time = models.DateTimeField("同步时间", default=timezone.now)
    STATUS_CHOICES = [(status.name, status.value) for status in StatusEnum]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=StatusEnum.NOT_STARTED.name)

    def __str__(self):
        return f"{self.id} - {self.status}"


class Host(models.Model):
    host_id = models.IntegerField(unique=True)
    host_name = models.CharField(max_length=100, default="")
    host_innerip = models.CharField(max_length=100, default="")
    host_outerip = models.CharField(max_length=100, default="")
    operator = models.CharField(max_length=100, default="")
    bak_operator = models.CharField(max_length=100, default="")
    cloud_vendor = models.CharField(max_length=100, default="")
    version = models.ForeignKey(Version, on_delete=models.CASCADE, null=True, related_name="hosts")


class Business(models.Model):
    biz_name = models.CharField(max_length=100, default="")
    biz_id = models.IntegerField(unique=True)
    version = models.ForeignKey(Version, on_delete=models.CASCADE, null=True, related_name="businesses")


class Set(models.Model):
    set_name = models.CharField(max_length=100, default="")
    set_id = models.IntegerField(unique=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="sets")
    version = models.ForeignKey(Version, on_delete=models.CASCADE, null=True, related_name="sets")


class Module(models.Model):
    module_name = models.CharField(max_length=100, default="")
    module_id = models.IntegerField(unique=True)
    set = models.ForeignKey(Set, on_delete=models.CASCADE, related_name="modules")
    hosts = models.ManyToManyField(Host, related_name="modules")
    version = models.ForeignKey(Version, on_delete=models.CASCADE, null=True, related_name="modules")
