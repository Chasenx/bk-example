from django.conf import settings
import logging

logger = logging.getLogger('app')

def create_search_files_job(client, dir, suffix, hosts):
    """
    创建查询文件作业
    :param client: Client
    :param dir: str
    :param suffix: str
    :param hosts: List[str]
    :returns job_instance_id: long
    """

    # 查询数据
    query = {
        "bk_scope_type": "biz",
        "bk_scope_id": "3",
        "job_plan_id": settings.SEARCH_JOB_PLAN_ID,
        "global_var_list": [
            {
                "name": "host",
                "server": {
                    "ip_list": [{"bk_cloud_id": 0, "ip": ip} for ip in hosts]
                }
            },
            {
                "name": "dir",
                "value": dir
            },
            {
                "name": "suffix",
                "value": suffix
            }
        ]
    }
    try:
        result = client.jobv3.execute_job_plan(**query)
        data = result.get("data")
    except Exception as e:
        return None

    if data:
        job_instance_id = data.get("job_instance_id")
        return job_instance_id
    else:
        return None


def check_job_status(client, job_instance_id):
    """
    检查作业状态
    :param client: Client
    :param job_instance_id: long
    :returns status: Boolean
    """
    query = {
        "bk_scope_type": "biz", 
        "bk_scope_id": "3",
        "job_instance_id": job_instance_id,
    }

    try:
        result = client.jobv3.get_job_instance_status(**query)
        data = result.get("data")
    except Exception as e:
        return False

    if data:
        status = data.get("finished", False)
        return status
    else:
        return False


def get_step_instance_id(client, job_instance_id):
    """
    获取 job_instance_id
    :param job_instance_id: long
    :returns step_instance_id: long
    """
    query = {
        "bk_scope_type": "biz", 
        "bk_scope_id": "3",
        "job_instance_id": job_instance_id,
    }

    try:
        result = client.jobv3.get_job_instance_status(**query)
        data = result.get("data")
    except Exception as e:
        return None

    if data:
        step_instance_list = data.get("step_instance_list")
        return step_instance_list[0]["step_instance_id"]
    else:
        return None


def get_job_result(client, job_instance_id, step_instance_id, host_id):
    """
    获取作业执行结果
    :param client: Client
    :param job_instance_id: long
    :param step_instance_id: long
    :returns result: str
    """
    query = {
        "bk_scope_type": "biz", 
        "bk_scope_id": "3",
        "job_instance_id": job_instance_id,
        "step_instance_id": step_instance_id,
        "bk_host_id": host_id
    }

    try:
        result = client.jobv3.get_job_instance_ip_log(**query)
        data = result.get("data")
    except Exception as e:
        return None

    if data:
        log_content = data.get("log_content")
        return log_content
    else:
        return None


def parse_log_data(log_data, ip):
    """
    清洗返回的查询文件日志数据
    :param log_data: str
    :param ip: str
    :returns result: str
    """
    file_names = []
    file_size = []
    log_data = log_data.split('\n')[1:] # 取出第一行内容

    for row in log_data:
        if row and row != '0':        # 排除空字符串和无搜索匹配结果的情况
            element = row.split()
            file_names.append(element[8])
            file_size.append(int(element[4]))
    result = {
        "ip": ip,
        "filenames": ', '.join(file_names),
        "size": sum(file_size)
    }
    return result


def create_backup_files_job(client, dir, files, hosts):
    """
    创建备份文件作业
    :param client: Client
    :param dir: str
    :param files: str
    :param hosts: List[str]
    :returns job_instance_id: long
    """

    # 查询数据
    query = {
        "bk_scope_type": "biz",
        "bk_scope_id": "3",
        "job_plan_id": settings.BACKUP_JOB_PLAN_ID,
        "global_var_list": [
            {
                "name": "host",
                "server": {
                    "ip_list": [{"bk_cloud_id": 0, "ip": ip} for ip in hosts]
                }
            },
            {
                "name": "dir",
                "value": dir
            },
            {
                "name": "files",
                "value": files
            }
        ]
    }
    try:
        result = client.jobv3.execute_job_plan(**query)
        data = result.get("data")
    except Exception as e:
        return None

    if data:
        job_instance_id = data.get("job_instance_id")
        return job_instance_id
    else:
        return None

