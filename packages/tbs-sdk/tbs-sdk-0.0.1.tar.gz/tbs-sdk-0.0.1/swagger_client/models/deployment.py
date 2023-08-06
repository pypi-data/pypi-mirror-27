from six import iteritems
from pprint import pformat


class Deployment(object):
    swagger_types = {
        'id': 'str',
        'name': 'str',
        'project': 'str',
        'created_at': 'str',
        'created_by': 'str',
        'config': 'object',
        'framework': 'str',
        'runtime': 'str',
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'project': 'project',
        'created_at': 'created_at',
        'created_by': 'created_by',
        'config': 'config',
        'framework': 'framework',
        'runtime': 'runtime',
    }

    def __init__(self, id=None, name=None, project=None, created_at=None, created_by=None, config=None, status=None, endpoint=None, framework=None, runtime=None):
        """
        Server - a model defined in Swagger
        """

        self._id = None
        self._name = None
        self._project = None
        self._created_at = None
        self._created_by = None
        self._config = None
        self._status = None
        self._endpoint = None
        self._framework = None
        self._runtime = None

        if id is not None:
          self.id = id
        self.name = name
        if project is not None:
          self.project = project
        if created_at is not None:
          self.created_at = created_at
        if created_by is not None:
          self.created_by = created_by
        if config is not None:
          self.config = config
        if status is not None:
          self.status = status
        if endpoint is not None:
            self.endpoint = endpoint
        if framework is not None:
            self.framework = framework
        if runtime is not None:
            self.runtime = runtime

    @property
    def id(self):
        """
        Gets the id of this Server.
        Server unique identifier in UUID format.

        :return: The id of this Server.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Server.
        Server unique identifier in UUID format.

        :param id: The id of this Server.
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this Server.
        Server name.

        :return: The name of this Server.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Server.
        Server name.

        :param name: The name of this Server.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def project(self):
        """
        Gets the project of this Server.
        Project name.

        :return: The project of this Server.
        :rtype: str
        """
        return self._project

    @project.setter
    def project(self, project):
        """
        Sets the project of this Server.
        Project name.

        :param project: The project of this Server.
        :type: str
        """

        self._project = project

    @property
    def created_at(self):
        """
        Gets the created_at of this Server.
        Date and time when server was created.

        :return: The created_at of this Server.
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this Server.
        Date and time when server was created.

        :param created_at: The created_at of this Server.
        :type: str
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """
        Gets the created_by of this Server.
        User that created server.

        :return: The created_by of this Server.
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this Server.
        User that created server.

        :param created_by: The created_by of this Server.
        :type: str
        """

        self._created_by = created_by

    @property
    def config(self):
        """
        Gets the config of this Server.
        Server configuration option. Values are jupyter, restful and cron.

        :return: The config of this Server.
        :rtype: object
        """
        return self._config

    @config.setter
    def config(self, config):
        """
        Sets the config of this Server.
        Server configuration option. Values are jupyter, restful and cron.

        :param config: The config of this Server.
        :type: object
        """

        self._config = config

    @property
    def status(self):
        """
        Gets the status of this Server.
        Server status, such as Running or Error.

        :return: The status of this Server.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this Server.
        Server status, such as Running or Error.

        :param status: The status of this Server.
        :type: str
        """
        allowed_values = ["Stopped", "Running", "Error"]
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def framework(self):
        return self._framework

    @framework.setter
    def framework(self, framework):

        self._framework = framework

    @property
    def runtime(self):
        return self._runtime

    @runtime.setter
    def runtime(self, runtime):

        self._runtime = runtime

    @property
    def endpoint(self):
        """
        Gets the endpoint of this Server.
        Server endpoint path.

        :return: The endpoint of this Server.
        :rtype: str
        """
        return self._endpoint

    @endpoint.setter
    def endpoint(self, endpoint):
        """
        Sets the endpoint of this Server.
        Server endpoint path.

        :param endpoint: The endpoint of this Server.
        :type: str
        """

        self._endpoint = endpoint
    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, Deployment):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
