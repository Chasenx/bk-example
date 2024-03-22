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

import logging
import os
import time
from datetime import datetime

import redis
from blueapps.account.decorators import login_exempt
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from blueking.component.shortcuts import get_client_by_request

from .celery_tasks import (async_create_backup_files_job, async_pull_cmdb,
                           get_topo, pull_cc_data_new)
from .job import (check_job_status, create_backup_files_job,
                  create_search_files_job, get_job_result,
                  get_step_instance_id, parse_log_data)
from .models import Backup, Business, Host, Module, Set, Version

logger = logging.getLogger("app")

# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页
    """
    return render(request, "index.html")


def sync_cmdb(request):
    """
    用于同步cmdb数据库数据
    """
    bk_token = request.COOKIES["bk_token"]
    if bk_token is None:
        data = {"status": "not login yet"}
        return JsonResponse(data)

    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PORT = int(os.environ.get("REDIS_PORT"))
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)
    lock_key = "celery_pull_cmdb"
    status = r.get(lock_key)

    if status is None:
        # 设置标志
        current_time = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
        r.set(lock_key, current_time, ex=100)
        # celery 异步拉取数据
        async_pull_cmdb.delay(bk_token)
        data = {"status": "start sync"}
    else:
        data = {"status": "syncing", "timestamp": status.decode("utf-8")}

    return JsonResponse(data)


def get_business(request):
    """
    获取所有业务
    """
    businesses = Business.objects.all()
    data = {
        "status": "success",
        "data": [{"biz_id": b.biz_id, "biz_name": b.biz_name} for b in businesses],
    }

    return JsonResponse(data)


def get_sets_by_biz(request):
    """
    获取业务下的集群
    :param business: int
    """
    if "business" in request.GET:
        business_id = request.GET["business"]
        # 判断是不是数字 # TODO
        sets = Business.objects.get(biz_id=business_id).sets.values(
            "set_id", "set_name"
        )
        response_data = {"status": "success", "data": list(sets) if list(sets) else []}
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Missing business parameter"}, status=400)


def get_modules_by_set(request):
    """
    获取集群下的模块
    :param set: int
    """
    if "set" in request.GET:
        set_id = request.GET["set"]

        modules = Set.objects.get(set_id=set_id).modules.values(
            "module_id", "module_name"
        )
        response_data = {"status": "success", "data": list(modules)}
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Missing set parameter"}, status=400)


def get_hosts(request):
    """
    获取主机列表
    :param business: int
    :param set: int
    :param module: int
    """
    # 分页
    page_size = request.GET.get("limit", 10)  # 提供默认值
    start = request.GET.get("start", 1)  # 提供默认值

    try:
        page_size = int(page_size)
        start = int(start)
    except ValueError:
        return JsonResponse({"message": "query error"})

    # 获取请求参数
    business_id = request.GET.get("business")
    set_id = request.GET.get("set")
    module_id = request.GET.get("module")

    if module_id:
        hosts = Module.objects.get(module_id=module_id).hosts.all()
    elif set_id:
        modules = Set.objects.get(set_id=set_id).modules.all()
        hosts = Host.objects.filter(modules__in=modules).order_by("host_id").distinct()
    elif business_id:
        sets = Business.objects.get(biz_id=business_id).sets.all()
        modules = Module.objects.filter(set__in=sets)
        hosts = Host.objects.filter(modules__in=modules).order_by("host_id").distinct()
    else:
        hosts = Host.objects.all()

    paginator = Paginator(hosts, page_size)  # page_size 为每页的对象数

    try:
        # 获取请求的页面
        page_objects = paginator.page(start)
    except EmptyPage:
        # 如果页码超出范围，展示最后一页的结果
        page_objects = paginator.page(paginator.num_pages)

    response_data = {
        "status": "success",
        "total": len(hosts),
        "count": len(page_objects),
        "data": list(page_objects.object_list.values()),
    }
    return JsonResponse(response_data)


def get_host_info(request):
    """
    获取主机详细信息
    :param host: int
    """
    host_id = request.GET.get("host")
    client = get_client_by_request(request)
    host_info = client.cc.get_host_base_info({"bk_host_id": host_id})

    return JsonResponse(host_info)


def search_files(request):
    """
    利用作业平台查询主机文件
    :param dir: str
    :param suffix: str
    :param host: str
    """
    host_dict = {
        "10.0.48.18": 863,
        "10.0.48.46": 864,
        "10.0.48.45": 865,
        "10.0.48.48": 867,
        "10.0.48.37": 868,
        "10.0.48.32": 869,
        "10.0.48.8": 870,
        "10.0.48.7": 871,
    }

    dir = request.GET.get("dir")
    suffix = request.GET.get("suffix")
    hosts = request.GET.get("hosts")

    if dir and suffix and hosts:
        hosts = hosts.split(",")  # 分开 host
        hosts = [h.strip() for h in hosts]  # 去除 IP 地址首位空格
        hosts = list(set(hosts))  # 去除重复 IP 地址

        # 限定主机查询文件
        for h in hosts:
            if h not in host_dict:
                return JsonResponse({"message": f"{h} can not execute"})

        client = get_client_by_request(request)

        # 创建查询任务
        job_instance_id = create_search_files_job(client, dir, suffix, hosts)

        # 等待任务完成
        while not check_job_status(client, job_instance_id):
            # TODO 想个办法解决这个 sleep 问题
            time.sleep(0.5)

        # 获取 step_instance_id
        step_instance_id = get_step_instance_id(
            client=client, job_instance_id=job_instance_id
        )

        # 获取结果
        file_info = []
        for h in hosts:
            result = get_job_result(
                client=client,
                job_instance_id=job_instance_id,
                step_instance_id=step_instance_id,
                host_id=host_dict[h],
            )
            if result:
                file_info.append(parse_log_data(result, h, dir))

        return JsonResponse({"data": file_info})

    return JsonResponse({"message": "query error"})


def backup_files(request):
    """
    利用作业平台备份主机文件
    :param dir: str
    :param suffix: str
    :param host: str
    """
    host_dict = {
        "10.0.48.18": 863,
        "10.0.48.46": 864,
        "10.0.48.45": 865,
        "10.0.48.48": 867,
        "10.0.48.37": 868,
        "10.0.48.32": 869,
        "10.0.48.8": 870,
        "10.0.48.7": 871,
    }

    bk_token = request.COOKIES["bk_token"]
    if bk_token is None:
        data = {"message": "not login yet"}
        return JsonResponse(data)

    dir = request.GET.get("dir")
    files = request.GET.get("files")
    hosts = request.GET.get("hosts")

    if dir and files and hosts:
        hosts = hosts.split(",")  # 分开 host
        hosts = [h.strip() for h in hosts]  # 去除 IP 地址首尾空格
        hosts = list(set(hosts))  # 去除重复 IP 地址

        # 限定主机备份文件
        for h in hosts:
            if h not in host_dict:
                return JsonResponse({"message": f"{h} is inactive"})

        # 创建文件备份任务 (同步实现)
        # job_instance_id = create_backup_files_job(client, dir, files, hosts)

        # 创建文件备份任务 (异步实现)
        username = request.user.username
        job_instance_id = async_create_backup_files_job.delay(
            bk_token, dir, files, hosts, username
        )

        return JsonResponse({"message": "add backup task"})

    return JsonResponse({"message": "query error"})


def backup_records(request):
    page_size = request.GET.get("limit", 10)  # 提供默认值
    start = request.GET.get("start", 1)  # 提供默认值

    try:
        page_size = int(page_size)
        start = int(start)
    except ValueError:
        return JsonResponse({"message": "query error"})

    objects = Backup.objects.all().order_by("-pk")  # 按主键倒序
    paginator = Paginator(objects, page_size)  # page_size 为每页的对象数

    try:
        # 获取请求的页面
        page_objects = paginator.page(start)
    except EmptyPage:
        # 如果页码超出范围，展示最后一页的结果
        page_objects = paginator.page(paginator.num_pages)

    response_data = {
        "status": "success",
        "total": Backup.objects.count(),
        "count": len(page_objects),
        "data": list(
            page_objects.object_list.values()
        ),  # 使用 object_list 获取 QuerySet
    }
    return JsonResponse(response_data)


def topo_tree(request):
    """
    输出拓扑结构
    """
    data = {"status": "success", "data": get_topo()}
    return JsonResponse(data)


@login_exempt
@csrf_exempt
def iam_business(request):
    """
    IAM 反向拉取接口
    """
    business = Business.objects.all()
    resources = {
        "code": 0,
        "message": "",
        "data": {
            "count": len(business),
            "results": [{"id": f'{b.biz_id}', "display_name": b.biz_name} for b in business],
        }
    }
    return JsonResponse(resources)


# @login_exempt
def test_json(request):
    """
    测试数据
    """

    # from home_application.celery_tasks import async_task
    # task_id = async_task.delay(1, 2)

    client = get_client_by_request(request)
    # biz_result = client.cc.search_business()
    # test_result = biz_result["data"]["info"][3]["operator"]
    # print(test_result == '')
    # import os
    # for key, value in os.environ.items():
    #     print(f"{key}: {value}")
    # logger.info('hhh')
    # query = {
    #     "bk_biz_id": 3,
    # }
    # result = client.cc.search_biz_inst_topo(**query)
    # 创建一个 Version 对象
    # from .models import Version
    # version = Version.objects.create()
    # from django.conf import settings
    bk_token = request.COOKIES["bk_token"]
    # 同步
    # pull_cc_data_new(bk_token=bk_token)

    # 输出拓扑结构

    # 鉴权（超级管理员和业务权限）
    from .utils import Permission, PermissionSU
    # result = Permission().is_super_user(request.user.username)
    # result = Permission().allowed_access_business(request.user.username, "3")

    # 获取申请权限 URL
    perission_su = PermissionSU()
    access_application = perission_su.make_no_resource_application("super_user_iam")
    url = perission_su.generate_apply_url(bk_token, access_application)

    data = {"web": "baidu", "url": "https://baidu.com/", "apply_url": url}

    return JsonResponse(data)
