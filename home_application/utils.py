from django.conf import settings
from iam import IAM, Action, Request, Resource, Subject
from iam.apply.models import (
    ActionWithoutResources,
    ActionWithResources,
    Application,
    RelatedResourceType,
    ResourceInstance,
    ResourceNode,
)

SYSTEM_ID = settings.APP_CODE
APP_CODE = settings.APP_CODE
APP_SECRET = settings.SECRET_KEY
BK_IAM_HOST = settings.BK_IAM_HOST
BK_PAAS_HOST = settings.BK_URL


class Permission:
    def __init__(self):
        self._iam = IAM(APP_CODE, APP_SECRET, BK_IAM_HOST, BK_PAAS_HOST)

    def _make_request_without_resources(self, username, action_id):
        request = Request(
            SYSTEM_ID,
            Subject("user", username),
            Action(action_id),
            None,
            None,
        )
        return request

    def _make_request_with_resources(self, username, action_id, resources):
        request = Request(
            SYSTEM_ID,
            Subject("user", username),
            Action(action_id),
            resources,
            None,
        )
        return request

    def is_super_user(self, username):
        """
        超级管理员权限
        """
        request = self._make_request_without_resources(username, "super_user_iam")
        return self._iam.is_allowed(request)

    def allowed_access_bu_make_request_without_resourcessiness(self, username, biz_id):
        """
        访问业务权限
        """
        r = Resource(SYSTEM_ID, "cc_biz", biz_id, {})
        resources = [r]
        request = self._make_request_with_resources(username, "access_biz", resources)
        return self._iam.is_allowed(request)


class PermissionSU:
    def __init__(self):
        self._iam = IAM(APP_CODE, APP_SECRET, BK_IAM_HOST, BK_PAAS_HOST)

    def make_no_resource_application(self, action_id):
        # 1. make application
        action = ActionWithoutResources(action_id)
        actions = [action]

        application = Application(SYSTEM_ID, actions)
        return application

    def make_resource_application(self, action_id, resource_type, resource_id, resource_name):
        # 1. make application
        # 这里支持带层级的资源, 例如 biz: 1/set: 2/host: 3
        # 如果不带层级, list中只有对应资源实例
        instance = ResourceInstance([ResourceNode(resource_type, resource_id, resource_name)])
        # 同一个资源类型可以包含多个资源
        related_resource_type = RelatedResourceType(SYSTEM_ID, resource_type, [instance])
        action = ActionWithResources(action_id, [related_resource_type])

        actions = [
            action,
        ]
        application = Application(SYSTEM_ID, actions)
        return application

    def generate_apply_url(self, bk_token, application):
        """
        处理无权限 - 跳转申请列表
        """
        # 2. get url
        ok, message, url = self._iam.get_apply_url(application, bk_token)
        if not ok:
            return "no"
        return url

    # def generate_apply_url(self, bk_username, application):
    #     """
    #     处理无权限 - 跳转申请列表, 使用bk_username
    #     """
    #     # 2. get url
    #     ok, message, url = self._iam.get_apply_url(application, bk_username=bk_username)
    #     if not ok:
    #         logger.error("iam generate apply url fail: %s", message)
    #         return IAM_APP_URL
    #     return url
