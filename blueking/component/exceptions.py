class ComponentBaseException(Exception):
    pass


class ComponentAPIException(ComponentBaseException):
    """Exception for Component API"""

    def __init__(self, api_obj, error_message, resp=None):
        self.api_obj = api_obj
        self.error_message = error_message
        self.resp = resp

        if self.resp is not None:
            error_message = "{}, resp={}".format(error_message, self.resp.text)
        super().__init__(error_message)
