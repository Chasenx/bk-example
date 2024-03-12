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
from .celery_tasks import async_pull_cmdb
import redis
from datetime import datetime

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


def sync_cmdb(request):
    """
    用于同步cmdb数据库数据, 后面需要实现成 celery 异步任务
    """
    bk_token = request.COOKIES["bk_token"]
    if bk_token is None:
        data = {"status": "not login yet"}
        return JsonResponse(data)

    # TODO: set redis dev env
    r = redis.Redis(host='192.168.50.209', port=6379, db=0)
    lock_key = 'celery_pull_cmdb'
    status = r.get(lock_key)

    if status is None:
        # 设置标志
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        r.set(lock_key, current_time, ex=100)
        # celery 异步实现
        async_pull_cmdb.delay(bk_token)
        data = {"status": "start to sync"}
    else:
        data = {"status": f"task start at {status.decode('utf-8')}"}
        
    return JsonResponse(data)


def get_business(request):
    """
    获取所有业务
    """
    unique_biz_ids = Host.objects.values('biz_id').distinct()
    data = {"status": "success", "data": list(unique_biz_ids.values("biz_id", "biz_name"))}

    return JsonResponse(data)


def get_sets_by_biz(request):
    """
    获取业务下的集群
    :param business: int
    """
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


def get_modules_by_set(request):
    """
    获取集群下的模块
    :param set: int
    """
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


def get_hosts(request):
    """
    获取主机列表
    :param business: int
    :param set: int
    :param module: int
    """
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
    # TODO: 做分页操作 limit page
    if not filters:
        hosts = Host.objects.all()
    else:
        # 根据过滤字典查询相应的记录
        hosts = Host.objects.filter(**filters)

    response_data = {
        "status": "success",
        'data': list(hosts.values())
    }
    return JsonResponse(response_data)


def get_host_info(request):
    """
    获取主机详细信息
    :param host: int
    """
    host_id = request.GET.get('host')
    client = get_client_by_request(request)
    host_info = client.cc.get_host_base_info({"bk_host_id": host_id})

    return JsonResponse(host_info)


@login_exempt
def test_json(request):
    """
    测试数据
    """

    from home_application.celery_tasks import async_task
    task_id = async_task.delay(1, 2)

    # client = get_client_by_request(request)
    # biz_result = client.cc.search_business()
    # test_result = biz_result["data"]["info"][3]["operator"]
    # print(test_result == '')
    
    data = {
        'web': 'baidu',
        'url': 'https://baidu.com/'
    }

    return JsonResponse(data)