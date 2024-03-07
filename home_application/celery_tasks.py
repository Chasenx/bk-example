from celery.task import task
from blueking.component.shortcuts import get_client_by_request
from .models import Host

@task()
def async_task(x, y):
    """
    test for celery
    """
    print('execute celery async task-----')
    print(x, y)


@task()
def async_pull_cmdb(request):
    pull_cc_data(request)


def setblank(data):
    if data is None:
        return ''
    else:
        return data


def pull_cc_data(request):
    """
    拉取CMDB数据
    """
    # TODO: 重构这个函数

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
        for set_data in set_info:
            set_id = set_data["bk_set_id"]
            set_name = set_data["bk_set_name"]

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
