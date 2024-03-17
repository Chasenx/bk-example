from celery.task import task
from blueking.component.shortcuts import get_client_by_bktoken
from .models import Host, Backup, Business, Set, Module, Version
import logging
import time
import redis
import os
from .job import create_backup_files_job
from django.conf import settings

logger = logging.getLogger('app')


@task()
def async_pull_cmdb(bk_token):
    pull_cc_data_new(bk_token)

    # 删除同步标记
    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = int(os.environ.get('REDIS_PORT'))
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)
    lock_key = 'celery_pull_cmdb'
    r.delete(lock_key)


@task()
def async_create_backup_files_job(bk_token, dir, files, hosts, username):
    # TODO: 备份冷却时间，不能一直点击
    logger.info(f'Create backup files job, dir: {dir}, files: {files}, hosts: {hosts}')

    client = get_client_by_bktoken(bk_token)
    job_instance_id = create_backup_files_job(client, dir, files, hosts)

    # 提取备份文件后缀
    file_list = files.split(',')
    first_file_name = file_list[0]
    suffix = first_file_name.split('.')[-1]
    
    # 添加备份记录表项
    bulk_backup = []
    for host in hosts:
        instance_info = {
            "host_ip": host,
            "dir": dir,
            "suffix": suffix,
            "backup_user": username,
            "backup_files": files,
            "job_link": f'{settings.JOB_LINK_PREFIX}{job_instance_id}',
            "job_instance_id": job_instance_id,
        }
        logger.info('create Backup object', instance_info)
        bulk_backup.append(Backup(**instance_info))

    Backup.objects.bulk_create(bulk_backup)


def setblank(data):
    return data if data else ''


def pull_cc_data(bk_token):
    """
    拉取CMDB数据
    """
    # TODO: 重构这个函数, 多线程查询 + bulk_create

    # 调用接口的客户端
    client = get_client_by_bktoken(bk_token)

    # 拉取biz
    try:
        biz_result = client.cc.search_business()
        print(biz_result)
        biz_info = biz_result["data"]["info"]
        assert(biz_info is not None)
    except:
        return
    
    
    # biz_info = [biz_info[0]]  # for ease
    for biz in biz_info:
        biz_id = biz.get("bk_biz_id")
        biz_name = biz.get("bk_biz_name", "")

        # 查找集群
        try:
            set_result = client.cc.search_set({"bk_biz_id": biz_id, "fields": ["bk_set_id", "bk_set_name"], "condition": {}, "page": {}})
            set_info = set_result["data"]["info"]
            assert(set_info is not None)
        except:
            return

        # set_info = [set_info[0]]  # for ease
        for set_data in set_info:
            set_id = set_data["bk_set_id"]
            set_name = set_data["bk_set_name"]

            # 查找模块
            try:
                module_result = client.cc.search_module({"bk_biz_id": biz_id, "bk_set_id": set_id, "fields": ["bk_module_id", "bk_module_name"], "condition": {}, "page": {}})
                module_info = module_result["data"]["info"]
                assert(module_info is not None)
            except:
                return
            
            # module_info = [module_info[0]]  # for ease
            for module in module_info:
                module_id = module["bk_module_id"]
                module_name = module["bk_module_name"]

                # 查找主机
                # for ease
                # biz_id = 3
                # set_id = 18
                # module_id = 80
                try:
                    host_result = client.cc.list_biz_hosts({
                        "bk_biz_id": biz_id, 
                        "bk_set_ids": [set_id],
                        "bk_module_ids": [module_id], 
                        "fields": ["bk_host_id", "bk_host_name", "bk_host_outerip", "bk_host_innerip", "operator", "bk_bak_operator", "bk_cloud_vendor"], 
                        "page": {"start": 0, "limit": 1000}
                    })
                    
                    host_info = host_result["data"]["info"]
                    assert(host_info is not None)
                except:
                    return

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


def update_business(bk_token, version):
    """
    拉取 CMDB, 更新 Business 表
    :returns biz_ids: List[int]
    """

    # 调用接口的客户端
    client = get_client_by_bktoken(bk_token)

    # 拉取所有业务
    try:
        biz_result = client.cc.search_business()
        logger.info(f'biz_result: {biz_result}')
        biz_info = biz_result["data"]["info"]
        assert(biz_info is not None)
    except Exception as e:
        logger.error(e, exc_info=True)
        return
    
    # biz_info = [biz_info[0]]  # for ease

    # 创建业务ORM
    biz_bulk = []
    for biz in biz_info:
        instance_info = {
            "biz_name": biz.get("bk_biz_name", ""),
            "biz_id": biz.get("bk_biz_id"),
            "version": version,
        }
        biz_bulk.append(Business(**instance_info))

    # 找出所有 biz_id
    biz_ids = [biz.biz_id for biz in biz_bulk]
    # 找出存在于数据库的 biz_id 的对象
    exist_bizs = Business.objects.filter(biz_id__in=biz_ids)

    # 转换成 biz_id->ORM , 方便后面处理
    exist_bizs_dict = {biz.biz_id: biz for biz in exist_bizs}

    bizs_to_update = []
    bizs_to_create = []

    for biz in biz_bulk:
        if biz.biz_id in exist_bizs_dict:
            # 添加到更新桶
            logger.info(f'update biz: {biz.biz_id}')
            exist_biz = exist_bizs_dict[biz.biz_id]
            exist_biz.biz_name = biz.biz_name
            exist_biz.version = biz.version
            bizs_to_update.append(exist_biz)
        else:
            # 添加到添加桶
            logger.info(f'create biz: {biz.biz_id}')
            bizs_to_create.append(biz)

    Business.objects.bulk_update(bizs_to_update, ['biz_name', 'version'])
    Business.objects.bulk_create(bizs_to_create)

    return biz_ids


def update_set(bk_token, biz_id):
    """
    拉取 CMDB, 更新 biz_id 内部的集群信息
    :returns set_ids: List[int]
    """
    biz = Business.objects.get(biz_id=biz_id)

    # 调用接口的客户端
    client = get_client_by_bktoken(bk_token)

    # 查找集群
    try:
        set_result = client.cc.search_set({"bk_biz_id": biz.biz_id, "fields": ["bk_set_id", "bk_set_name"], "condition": {}, "page": {}})
        set_info = set_result["data"]["info"]
        assert(set_info is not None)
    except Exception as e:
        logger.error(e, exc_info=True)
        return

    # 创建集群 ORM
    set_bulk = []
    for set in set_info:
        instance_info = {
            "set_name": set.get("bk_set_name", ""),
            "set_id": set.get("bk_set_id"),
            "version": biz.version,
            "business": biz
        }
        set_bulk.append(Set(**instance_info))

    # 找出所有 set_id
    set_ids = [set.set_id for set in set_bulk]
    # 找出存在于数据库的 set_id 的对象
    exist_sets = Set.objects.filter(set_id__in=set_ids)

    # 转换成 set_id->ORM , 方便后面处理
    exist_sets_dict = {set.set_id: set for set in exist_sets}

    sets_to_update = []
    sets_to_create = []

    for set in set_bulk:
        if set.set_id in exist_sets_dict:
            # 添加到更新桶
            logger.info(f'update set: {set.set_id}')
            exist_set = exist_sets_dict[set.set_id]
            exist_set.set_name = set.set_name
            exist_set.version = set.version
            exist_set.business = set.business
            sets_to_update.append(exist_set)
        else:
            # 添加到添加桶
            logger.info(f'create set: {set.set_id}')
            sets_to_create.append(set)

    Set.objects.bulk_update(sets_to_update, ['set_name', 'version', 'business'])
    Set.objects.bulk_create(sets_to_create)
    
    return set_ids


def update_module(bk_token, set_id):
    """
    拉取 CMDB, 更新 set_id 内部的模块信息
    :returns module_ids: List[int]
    """
    set = Set.objects.get(set_id=set_id)

    # 调用接口的客户端
    client = get_client_by_bktoken(bk_token)

    # 查找模块
    try:
        module_result = client.cc.search_module({"bk_biz_id": set.business.biz_id, "bk_set_id": set.set_id, "fields": ["bk_module_id", "bk_module_name"], "condition": {}, "page": {}})
        module_info = module_result["data"]["info"]
        assert(module_info is not None)
    except Exception as e:
        logger.error(e, exc_info=True)
        return
    
    # 创建模块 ORM
    module_bulk = []
    for module in module_info:
        instance_info = {
            "module_name": module.get("bk_module_name", ""),
            "module_id": module.get("bk_module_id"),
            "version": set.version,
            "set": set
        }
        module_bulk.append(Module(**instance_info))

    # 找出所有 module_id
    module_ids = [module.module_id for module in module_bulk]
    # 找出存在于数据库的 module_id 的对象
    exist_modules = Module.objects.filter(module_id__in=module_ids)

    # 转换成 module_id->ORM , 方便后面处理
    exist_modules_dict = {module.module_id: module for module in exist_modules}

    modules_to_update = []
    modules_to_create = []

    for module in module_bulk:
        if module.module_id in exist_modules_dict:
            # 添加到更新桶
            logger.info(f'update module: {module.module_id}')
            exist_module = exist_modules_dict[module.module_id]
            exist_module.module_name = module.module_name
            exist_module.version = module.version
            exist_module.set = module.set
            modules_to_update.append(exist_module)
        else:
            # 添加到添加桶
            logger.info(f'create module: {module.module_id}')
            modules_to_create.append(module)

    Module.objects.bulk_update(modules_to_update, ['module_name', 'version', 'set'])
    Module.objects.bulk_create(modules_to_create)
    
    return module_ids


def update_host(bktoken, module_id):
    """
    拉取 CMDB, 更新 module_id 内部的主机信息
    :returns host_ids: List[int]
    """
    module = Module.objects.get(module_id=module_id)

    # 调用接口的客户端
    client = get_client_by_bktoken(bktoken)

    # 查找主机
    try:
        host_result = client.cc.list_biz_hosts({
            "bk_biz_id": module.set.business.biz_id, 
            "bk_set_ids": [module.set.set_id],
            "bk_module_ids": [module.module_id], 
            "fields": ["bk_host_id", "bk_host_name", "bk_host_outerip", "bk_host_innerip", "operator", "bk_bak_operator", "bk_cloud_vendor"], 
            "page": {"start": 0, "limit": 1000}
        })
        host_info = host_result["data"]["info"]
        assert(host_info is not None)
    except Exception as e:
        logger.error(e, exc_info=True)
        return

    # 创建主机 ORM
    host_bulk = []
    for host in host_info:
        instance_info = {
            "host_name": setblank(host["bk_host_name"]),
            "host_id": host["bk_host_id"],
            "host_innerip": setblank(host["bk_host_innerip"]),
            "host_outerip": setblank(host["bk_host_outerip"]),
            "operator": setblank(host["operator"]),
            "bak_operator": setblank(host["bk_bak_operator"]),
            "cloud_vendor": setblank(host["bk_cloud_vendor"]),
            "version": module.version,
        }
        host_bulk.append(Host(**instance_info))

    # 找出所有 host_id
    host_ids = [host.host_id for host in host_bulk]

    # 找出模块内所有 host_id
    exist_hosts = list(module.hosts.all())

    # 转换成 host_id->ORM , 方便后面处理
    exist_hosts_dict = {host.host_id: host for host in exist_hosts}
    logger.info(f'len of exist_hosts_dict: {len(exist_hosts_dict)}')

    hosts_to_update = []
    hosts_to_create = []
    hosts_to_remove = []

    for host in host_bulk:
        if host.host_id in exist_hosts_dict:
            # 添加到更新桶
            logger.info(f'update host: {host.host_id}')
            exist_host = exist_hosts_dict[host.host_id]
            exist_host.host_name = host.host_name
            exist_host.host_innerip = host.host_innerip
            exist_host.host_outerip = host.host_outerip
            exist_host.operator = host.operator
            exist_host.bak_operator = host.bak_operator
            exist_host.cloud_vendor = host.cloud_vendor
            exist_host.version = host.version
            hosts_to_update.append(exist_host)
        elif Host.objects.filter(host_id=host.host_id).exists():
            # 之前未关联但已经存在的主机
            exist_host = Host.objects.get(host_id=host.host_id)
            exist_host.host_name = host.host_name
            exist_host.host_innerip = host.host_innerip
            exist_host.host_outerip = host.host_outerip
            exist_host.operator = host.operator
            exist_host.bak_operator = host.bak_operator
            exist_host.cloud_vendor = host.cloud_vendor
            exist_host.version = host.version
            module.hosts.add(exist_host)       # 添加关联
            hosts_to_update.append(exist_host)
        else:
            # 添加到添加桶   TODO: 这里有问题，不应该直接添加到数据库
            logger.info(f'create host: {host.host_id}')
            host.save()
            hosts_to_create.append(host)
    
    # 添加到删除桶
    for exist_host in exist_hosts:
        if exist_host.host_id not in host_ids:
            logger.info(f'remove host: {exist_host.host_id}')
            hosts_to_remove.append(exist_host)
    
    Host.objects.bulk_update(hosts_to_update, ['host_name', 'host_innerip', 'host_outerip', 'operator', 'bak_operator', 'cloud_vendor', 'version'])
    # Host.objects.bulk_create(hosts_to_create)
    module.hosts.add(*hosts_to_create)
    module.hosts.remove(*hosts_to_remove)
    
    return host_ids


def pull_cc_data_new(bk_token): 
    # 创建一个 Version
    version = Version.objects.create()
    logger.info('create a new verison')

    # 开始同步
    version.status = Version.StatusEnum.SYNCING.name
    version.save()

    try:
        # 更新 Business
        biz_ids = update_business(bk_token, version)

        # 循环更新集群
        for biz in biz_ids:
            set_ids = update_set(bk_token, biz)

            # 循环更新模块
            for set in set_ids:
                module_ids = update_module(bk_token, set)

                # 循环更新主机
                for module_id in module_ids:
                    host_ids = update_host(bk_token, module_id)
    except Exception as e:
        logger.error(e, exc_info=True)
        logger.error('ayncing failed')
        version.status = Version.StatusEnum.FAIL.name
        version.save()

    version.status = Version.StatusEnum.SUCCESS.name
    version.save()
    logger.info('ayncing success')

    # 删除旧版本数据
    outdated_hosts = Host.objects.exclude(version=version)

    for host in outdated_hosts:
        host.modules.clear()
        host.delete()

    # 接下来删除其他模型的过时对象
    for model in [Business, Set, Module]:  # Host已经处理过了
        outdated_objects = model.objects.exclude(version=version)
        outdated_objects.delete()


def get_topo():
    '''
    输出拓扑结构
    '''
    topology = []

    # 遍历所有业务
    for business in Business.objects.all():
        business_dict = {
            "bk_inst_name": business.biz_name, 
            "bk_biz_id": business.biz_id, 
            "children": [] 
        }
        
        for set in business.sets.all():
            set_dict = {
                "bk_inst_name": set.set_name, 
                "bk_biz_id":business.biz_id,
                "bk_set_id": set.set_id, 
                "children": []
            }
            
            for module in set.modules.all():
                # 排除没有主机的模块
                if module.hosts.exists():
                    module_dict = {
                        "bk_inst_name": module.module_name, 
                        "bk_biz_id":business.biz_id,
                        "bk_set_id": set.set_id,
                        "bk_module_id": module.module_id,
                        "children": []
                    }
                    set_dict["children"].append(module_dict)
            
            if len(set_dict["children"]) > 0:
                business_dict["children"].append(set_dict)
        
        if len(business_dict["children"]) > 0:
            topology.append(business_dict)

    return topology
