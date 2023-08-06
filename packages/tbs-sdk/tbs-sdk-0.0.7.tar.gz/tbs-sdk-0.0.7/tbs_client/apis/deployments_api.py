from six import iteritems
from ..configuration import Configuration
from ..api_client import ApiClient


class DeploymentsApi(object):
    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def deployments_create_with_http_info(self, namespace, project,  **kwargs):
        all_params = ['namespace', 'project','deployment_data']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method deployments_create" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'namespace' is set
        if ('namespace' not in params) or (params['namespace'] is None):
            raise ValueError("Missing the required parameter `namespace` when calling `create`")

        # verify the required parameter 'project' is set
        if ('project' not in params) or (params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `deployments_create`")
        collection_formats = {}

        path_params = {}
        if 'namespace' in params:
            path_params['namespace'] = params['namespace']

        if 'project' in params:
            path_params['project'] = params['project']

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'deployment_data' in params:
            body_params = params['deployment_data']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client. \
            select_header_accept(['application/json', 'text/html'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client. \
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['jwt']

        return self.api_client.call_api('/v1/{namespace}/projects/{project}/deployments/', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='Deployment',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def deployments_create(self, namespace, project, **kwargs):
        kwargs['_return_http_data_only'] = True
        (data) = self.deployments_create_with_http_info(namespace, project, **kwargs)
        return data

    def deployments_deploy_with_http_info(self, namespace, project, deployment, **kwargs):
        all_params = ['namespace', 'project', 'deployment']
        all_params.append("callback")
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method deployments_start" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'project' is set
        if ('project' not in params) or (params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `deployments_deploy`")
        # verify the required parameter 'namespace' is set
        if ('namespace' not in params) or (params['namespace'] is None):
            raise ValueError("Missing the required parameter `namespace` when calling `deployments_deploy`")
        # verify the required parameter 'deployment' is set
        if ('deployment' not in params) or (params['deployment'] is None):
            raise ValueError("Missing the required parameter `deployment` when calling `deployments_deploy`")

        collection_formats = {}

        path_params = {}
        if 'namespace' in params:
            path_params['namespace'] = params['namespace']
        if 'project' in params:
            path_params['project'] = params['project']
        if 'deployment' in params:
            path_params['deployment'] = params['deployment']

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client. \
            select_header_accept(['application/json', 'text/html'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client. \
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['jwt']

        return self.api_client.call_api('/v1/{namespace}/projects/{project}/deployments/{deployment}/deploy/', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type=None,
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def deployments_deploy(self, namespace, project, deployment, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.deployments_deploy_with_http_info(namespace, project, deployment, **kwargs)
        else:
            (data) = self.deployments_deploy_with_http_info(namespace, project, deployment, **kwargs)
            return data

    def deployments_read(self, project, namespace, deployment, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.deployments_read_with_http_info(project, namespace, deployment, **kwargs)
        else:
            (data) = self.deployments_read_with_http_info(project, namespace, deployment, **kwargs)
            return data

    def deployments_read_with_http_info(self, project, namespace, deployment, **kwargs):
        all_params = ['project', 'namespace', 'deployment']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method deployments_read" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'project' is set
        if ('project' not in params) or (params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `deployments_read`")
        # verify the required parameter 'namespace' is set
        if ('namespace' not in params) or (params['namespace'] is None):
            raise ValueError("Missing the required parameter `namespace` when calling `deployments_read`")
        # verify the required parameter 'deployment' is set
        if ('deployment' not in params) or (params['deployment'] is None):
            raise ValueError("Missing the required parameter `deployment` when calling `deployments_read`")


        collection_formats = {}

        path_params = {}
        if 'project' in params:
            path_params['project'] = params['project']
        if 'namespace' in params:
            path_params['namespace'] = params['namespace']
        if 'deployment' in params:
            path_params['deployment'] = params['deployment']

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/html'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['jwt']

        return self.api_client.call_api('/v1/{namespace}/projects/{project}/deployments/{deployment}/', 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='Deployment',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def deployments_delete(self, project, namespace, deployment, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.deployments_delete_with_http_info(project, namespace, deployment, **kwargs)
        else:
            (data) = self.deployments_delete_with_http_info(project, namespace, deployment, **kwargs)
            return data

    def deployments_delete_with_http_info(self, project, namespace, deployment, **kwargs):
        all_params = ['project', 'namespace', 'deployment']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method deployments_delete" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'project' is set
        if ('project' not in params) or (params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `deployments_delete`")
        # verify the required parameter 'namespace' is set
        if ('namespace' not in params) or (params['namespace'] is None):
            raise ValueError("Missing the required parameter `namespace` when calling `deployments_delete`")
        # verify the required parameter 'deployment' is set
        if ('deployment' not in params) or (params['deployment'] is None):
            raise ValueError("Missing the required parameter `deployment` when calling `deployments_delete`")


        collection_formats = {}

        path_params = {}
        if 'project' in params:
            path_params['project'] = params['project']
        if 'namespace' in params:
            path_params['namespace'] = params['namespace']
        if 'deployment' in params:
            path_params['deployment'] = params['deployment']

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/html'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['jwt']

        return self.api_client.call_api('/v1/{namespace}/projects/{project}/deployments/{deployment}/', 'DELETE',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type=None,
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def deployments_list(self, project, namespace, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.deployments_list_with_http_info(project, namespace, **kwargs)
        else:
            (data) = self.deployments_list_with_http_info(project, namespace, **kwargs)
            return data

    def deployments_list_with_http_info(self, project, namespace, **kwargs):
        all_params = ['project', 'namespace', 'limit', 'offset', 'name', 'ordering']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method deployments_list" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'project' is set
        if ('project' not in params) or (params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `deployments_list`")
        # verify the required parameter 'namespace' is set
        if ('namespace' not in params) or (params['namespace'] is None):
            raise ValueError("Missing the required parameter `namespace` when calling `deployments_list`")

        collection_formats = {}

        path_params = {}
        if 'project' in params:
            path_params['project'] = params['project']
        if 'namespace' in params:
            path_params['namespace'] = params['namespace']

        query_params = []
        if 'limit' in params:
            query_params.append(('limit', params['limit']))
        if 'offset' in params:
            query_params.append(('offset', params['offset']))
        if 'name' in params:
            query_params.append(('name', params['name']))
        if 'ordering' in params:
            query_params.append(('ordering', params['ordering']))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client. \
            select_header_accept(['application/json', 'text/html'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client. \
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['jwt']

        return self.api_client.call_api('/v1/{namespace}/projects/{project}/deployments/', 'GET',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='list[Server]',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def deployments_update(self, project, namespace, deployment, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.deployments_update_with_http_info(project, namespace, deployment, **kwargs)
        else:
            (data) = self.deployments_update_with_http_info(project, namespace, deployment, **kwargs)
            return data

    def deployments_update_with_http_info(self, project, namespace, deployment, **kwargs):
        all_params = ['project', 'namespace', 'deployment', 'deployment_data']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method deployments_update" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'project' is set
        if ('project' not in params) or (params['project'] is None):
            raise ValueError("Missing the required parameter `project` when calling `deployments_update`")
        # verify the required parameter 'namespace' is set
        if ('namespace' not in params) or (params['namespace'] is None):
            raise ValueError("Missing the required parameter `namespace` when calling `deployments_update`")
        # verify the required parameter 'deployment' is set
        if ('deployment' not in params) or (params['deployment'] is None):
            raise ValueError("Missing the required parameter `deployment` when calling `deployments_update`")


        collection_formats = {}

        path_params = {}
        if 'project' in params:
            path_params['project'] = params['project']
        if 'namespace' in params:
            path_params['namespace'] = params['namespace']
        if 'deployment' in params:
            path_params['deployment'] = params['deployment']

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'deployment_data' in params:
            body_params = params['deployment_data']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/html'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['jwt']

        return self.api_client.call_api('/v1/{namespace}/projects/{project}/deployments/{deployment}/', 'PATCH',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='Deployment',
                                        auth_settings=auth_settings,
                                        callback=params.get('callback'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
