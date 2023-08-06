

class DeploymentData(object):
    swagger_types = {
        'name': 'str',
        'config': 'DeploymentConfig',
        'runtime': 'str',
        'framework': 'str'
    }

    attribute_map = {
        'name': 'name',
        'config': 'config',
        'runtime': 'runtime',
        'framework': 'framework'
    }

    def __init__(self, name=None, config=None, runtime=None, framework=None):
        """
        ProjectData - a model defined in Swagger
        """

        self._name = None
        self._config = None
        self._runtime = None
        self._framework = None

        self.name = name

        if config is not None:
            self.config = config

        if runtime is not None:
            self.runtime = runtime

        if framework is not None:
            self.framework = framework

    @property
    def name(self):
        """
        Gets the name of this ServerData.
        Server name.

        :return: The name of this ServerData.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ServerData.
        Server name.

        :param name: The name of this ServerData.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def config(self):
        """
        Gets the name of this ServerData.
        Server name.

        :return: The name of this ServerData.
        :rtype: str
        """
        return self._config

    @config.setter
    def config(self, config):
        """
        Sets the name of this ServerData.
        Server name.

        :param name: The name of this ServerData.
        :type: str
        """
        if config is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._config = config

    @property
    def runtime(self):
        """
        Gets the name of this ServerData.
        Server name.

        :return: The name of this ServerData.
        :rtype: str
        """
        return self._runtime

    @runtime.setter
    def runtime(self, runtime):
        """
        Sets the name of this ServerData.
        Server name.

        :param name: The name of this ServerData.
        :type: str
        """
        if runtime is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._runtime = runtime

    @property
    def framework(self):
        """
        Gets the name of this ServerData.
        Server name.

        :return: The name of this ServerData.
        :rtype: str
        """
        return self._framework

    @framework.setter
    def framework(self, framework):
        """
        Sets the name of this ServerData.
        Server name.

        :param name: The name of this ServerData.
        :type: str
        """
        if framework is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._framework = framework