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

from django.shortcuts import render
from django.http import HttpResponse
from blueapps.account.decorators import login_exempt

# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页
    """
    # return render(request, "home_application/index_home.html")
    return render(request, "index.html")


def dev_guide(request):
    """
    开发指引
    """
    return render(request, "home_application/dev_guide.html")


def contact(request):
    """
    联系页
    """
    return render(request, "home_application/contact.html")


def hello(request):
    """
    测试用的hello world
    """
    from blueking.component.shortcuts import get_client_by_request

    # 需提供 django request，client 可从 request 中获取当前用户名或从 Cookies 中获取用户登录态；
    # 并且，支持从 django settings 获取默认的 bk_app_code、bk_app_secret、endpoint，也可通过参数指定。
    client = get_client_by_request(request)

    # 设置是否访问第三方系统的测试环境，默认值为False，访问其正式环境
    # client.set_use_test_env(True)

    # 设置访问组件API的超时时间，单位秒
    # client.set_timeout(10)

    host_id = "869"
    result = client.cc.list_biz_hosts({"bk_biz_id": "3", "bk_module_ids": [80], "fields": ["bk_host_id"], "page": {"start": 0, "limit": 100}})
    print(result)
    
    return HttpResponse(f'{result}')


def test_json(request):
    from django.http import JsonResponse
    data = {
        'aa': 10,
        'bb':20
    }
    return JsonResponse(data)