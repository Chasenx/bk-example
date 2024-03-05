# -*- coding: utf-8 -*-
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

from django.db import models

class TestModel(models.Model):
    data = models.CharField(max_length=200)
    count = models.IntegerField()
    pub_date = models.DateTimeField("date published")


class Host(models.Model):
    biz_name = models.CharField(max_length=100, default='')
    biz_id = models.IntegerField()
    set_id = models.IntegerField()
    set_name = models.CharField(max_length=100, default='')
    module_id = models.IntegerField()
    module_name = models.CharField(max_length=100, default='')
    host_id = models.IntegerField(unique=True)
    host_name = models.CharField(max_length=100, default='')
    host_innerip = models.CharField(max_length=100, default='')
    host_outerip = models.CharField(max_length=100, default='')
    operator = models.CharField(max_length=100, default='')
    bak_operator = models.CharField(max_length=100, default='')
    cloud_vendor = models.CharField(max_length=100, default='')
