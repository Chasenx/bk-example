from django.conf import settings
from iam import IAM, Request, Subject, Action, Resource

SYSTEM_ID = settings.APP_CODE
APP_CODE = settings.APP_CODE
APP_SECRET = settings.SECRET_KEY
BK_IAM_HOST = settings.BK_IAM_HOST
BK_PAAS_HOST = settings.BK_URL


class Permission(object):
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

    def allowed_develop_app(self, username, app_code):
        """
        带资源的操作
        """
        r = Resource(SYSTEM_ID, 'app', app_code, {})
        resources = [r]
        request = self._make_request_with_resources(username, "develop_app", resources)
        return self._iam.is_allowed(request)