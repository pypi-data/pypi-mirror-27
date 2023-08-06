

class DeploymentConfig(object):
    swagger_types = {
        'handler': "str",
        'files': "list",
        'endpoint': "str",
        'resource_id': "str",
        'rest_api_id': "str",
        'function_arn': "str"
    }

    attribute_map = {
        'handler': 'handler',
        'files': 'files',
        'endpoint': 'endpoint',
        'resource_id': 'resource_id',
        'rest_api_id': 'rest_api_id',
        'function_arn': 'function_arn'
    }

    def __init__(self, handler=None, files=None, endpoint=None, resource_id=None, rest_api_id=None, function_arn=None):
        self._handler = None
        self._files = None
        self._endpoint = None
        self._resource_id = None
        self._rest_api_id = None
        self._function_arn = None

        if handler is not None:
            self.handler = handler

        if files is not None:
            self.files = files

        if endpoint is not None:
            self.endpoint = endpoint

        if resource_id is not None:
            self.resource_id = resource_id

        if rest_api_id is not None:
            self.rest_api_id = None

        if function_arn is not None:
            self.function_arn = function_arn

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, handler):
        self._handler = handler

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, files):
        self._files = files

    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, endpoint):
        self._endpoint = endpoint

    @property
    def resource_id(self):
        return self._resource_id

    @resource_id.setter
    def resource_id(self, resource_id):
        self._resource_id = resource_id

    @property
    def rest_api_id(self):
        return self._rest_api_id

    @rest_api_id.setter
    def rest_api_id(self, rest_api_id):
        self._rest_api_id = rest_api_id

    @property
    def function_arn(self):
        return self._function_arn

    @function_arn.setter
    def function_arn(self, function_arn):
        self._function_arn = function_arn
