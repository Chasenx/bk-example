from ..base import ComponentAPI


class CollectionsUSERMANAGE:
    """Collections of USERMANAGE APIS"""

    def __init__(self, client):
        self.client = client

        self.department_ancestor = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/usermanage/department_ancestor/",
            description="查询部门全部祖先 (旧版接口，不推荐使用，后续会下架，请尽快迁移)",
        )
        self.list_department_profiles = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/usermanage/list_department_profiles/",
            description="查询部门的用户信息 (v2)",
        )
        self.list_departments = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/usermanage/list_departments/",
            description="查询部门 (v2)",
        )
        self.list_profile_departments = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/usermanage/list_profile_departments/",
            description="查询用户的部门信息 (v2)",
        )
        self.list_users = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/usermanage/list_users/",
            description="查询用户 (v2)",
        )
        self.retrieve_department = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/usermanage/retrieve_department/",
            description="查询单个部门信息 (v2)",
        )
        self.retrieve_user = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/usermanage/retrieve_user/",
            description="查询单个用户信息 (v2)",
        )
