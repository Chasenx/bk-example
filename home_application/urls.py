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

from django.conf.urls import url

from . import views

# example
urlpatterns = (
    url(r"^$", views.home),
    url(r"^dev-guide/$", views.dev_guide),
    url(r"^contact/$", views.contact),
    url(r'^test-json/$', views.test_json),
    url(r'^sync-cmdb/$', views.sync_cmdb),
    url(r'^business/$', views.get_business),
    url(r'^set$', views.get_sets_by_biz),
    url(r'^module$', views.get_modules_by_set),
    url(r'^hosts$', views.get_hosts),
    url(r'^host-info$', views.get_host_info),
    url(r'^search-files$', views.search_files),
    url(r'^backup-files$', views.backup_files),
    url(r'^backup-records$', views.backup_records),
    url(r'^topo$', views.topo_tree),
)

# urlpatterns = [
#     url(r'^$', views.hello),
#     url(r'^test-json/$', views.test_json)
# ]
