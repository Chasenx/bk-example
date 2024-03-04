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
from blueking.component.shortcuts import get_client_by_request
from .models import TestModel, Host
from django.http import JsonResponse

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


def setblank(data):
    if data is None:
        return ''
    else:
        return data


def pull_cc_data(request):
    # 拉取biz
    client = get_client_by_request(request)
    biz_result = client.cc.search_business()
    biz_info = biz_result["data"]["info"]
    
    # biz_info = [biz_info[0]]  # for ease
    for biz in biz_info:
        biz_id = biz["bk_biz_id"]
        biz_name = biz["bk_biz_name"]

        # 查找集群
        set_result = client.cc.search_set({"bk_biz_id": biz_id, "fields": ["bk_set_id", "bk_set_name"], "condition": {}, "page": {}})
        set_info = set_result["data"]["info"]

        # set_info = [set_info[0]]  # for ease
        for setData in set_info:
            set_id = setData["bk_set_id"]
            set_name = setData["bk_set_name"]

            # 查找模块
            module_result = client.cc.search_module({"bk_biz_id": biz_id, "bk_set_id": set_id, "fields": ["bk_module_id", "bk_module_name"], "condition": {}, "page": {}})
            module_info = module_result["data"]["info"]
            
            # module_info = [module_info[0]]  # for ease
            for module in module_info:
                module_id = module["bk_module_id"]
                module_name = module["bk_module_name"]

                # 查找主机
                # for ease
                # biz_id = 3
                # set_id = 18
                # module_id = 80
                host_result = client.cc.list_biz_hosts({
                    "bk_biz_id": biz_id, 
                    "bk_set_ids": [set_id],
                    "bk_module_ids": [module_id], 
                    "fields": ["bk_host_id", "bk_host_name", "bk_host_outerip", "bk_host_innerip", "operator", "bk_bak_operator", "bk_cloud_vendor"], 
                    "page": {"start": 0, "limit": 1000}
                })
                
                host_info = host_result["data"]["info"]

                # 建立　ORM　模型
                for host in host_info:
                    host_id = host["bk_host_id"]
                    host_name = setblank(host["bk_host_name"])

                    orm_data = {
                        "biz_id": biz_id,
                        "biz_name": biz_name,
                        "set_id": set_id,
                        "set_name": set_name,
                        "module_id": module_id,
                        "module_name": module_name,
                        "host_id": host_id,
                        "host_name": host_name,
                        "host_innerip": setblank(host["bk_host_innerip"]),
                        "host_outerip": setblank(host["bk_host_outerip"]),
                        "operator": setblank(host["operator"]),
                        "bak_operator": setblank(host["bk_bak_operator"]),
                        "cloud_vendor": setblank(host["bk_cloud_vendor"]),
                    }

                    if Host.objects.filter(host_id=host_id).exists():
                        hostORM = Host.objects.filter(host_id=host_id).update(**orm_data)
                    else:
                        hostORM = Host.objects.create(**orm_data)


def sync_cmdb(request):
    """
    用于同步cmdb数据库数据, 后面需要实现成 celery 异步任务
    """
    # 同步实现
    pull_cc_data(request)
    data = {"status": "success"}

    return JsonResponse(data)


@login_exempt
def get_business(request):
    unique_biz_ids = Host.objects.values('biz_id').distinct()
    data = {"status": "success", "data": list(unique_biz_ids.values("biz_id", "biz_name"))}

    return JsonResponse(data)


@login_exempt
def get_sets_by_biz(request):
    if 'business' in request.GET:
        business_id = request.GET['business']
        # 判断是不是数字 # TODO
        sets = Host.objects.filter(biz_id=business_id).values('set_id', 'set_name').distinct()
        response_data = {
            "status": "success",
            'data': list(sets)
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Missing business parameter'}, status=400)


@login_exempt
def get_modules_by_set(request):
    if 'set' in request.GET:
        set_id = request.GET['set']
        
        modules = Host.objects.filter(set_id=set_id).values('module_id', 'module_name').distinct()
        
        response_data = {
            "status": "success",
            'data': list(modules)
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Missing set parameter'}, status=400)


@login_exempt
def get_hosts(request):
    # 获取请求参数
    business_id = request.GET.get('business')
    set_id = request.GET.get('set')
    module_id = request.GET.get('module')

    # 创建一个过滤字典，只包含提供的参数
    filters = {}
    if business_id:
        filters['biz_id'] = business_id
    if set_id:
        filters['set_id'] = set_id
    if module_id:
        filters['module_id'] = module_id

    # 如果没有任何参数提供，则返回全部记录
    if not filters:
        hosts = Host.objects.all()
    else:
        # 根据过滤字典查询相应的记录
        hosts = Host.objects.filter(**filters)

    # 假设你希望返回查询到的记录的某些字段
    response_data = {
        "status": "success",
        'data': list(hosts.values())
    }
    return JsonResponse(response_data)


def test_json(request):
    from django.utils import timezone
    
    data = {
        'website': 'baidu',
        'url': 'https://baidu.com/'
    }

    return JsonResponse(data)