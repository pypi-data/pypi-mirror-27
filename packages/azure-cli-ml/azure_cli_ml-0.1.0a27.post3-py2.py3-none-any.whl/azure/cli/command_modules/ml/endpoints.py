# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import requests
import time
from azure.cli.core.util import CLIError
from .package import _package_create
from ._constants import SUCCESS_RETURN_CODE
from ._endpoints_utill import MMS_ENDPOINT_URL
from ._host_account_util import get_host_account_token
from ._constants import MMS_OPERATION_URL
from ._util import cli_context
from ._util import get_json
from ._util import get_sub_and_account_info


def endpoint_create(package_id, endpoint_name, kube_config, acr_pull_secret, acs_master_url, acs_agent_url, driver_file,
                    model_id, model_name, model_file, model_tags, model_description, package_description, schema_file,
                    dependencies, runtime, verb, context=cli_context):
    try:
        base_url, subscription, resource_group, host_account_name = get_sub_and_account_info()
    except CLIError as exc:
        raise exc

    _endpoint_create(package_id, endpoint_name, kube_config, acr_pull_secret, acs_master_url, acs_agent_url,
                     driver_file, model_id, model_name, model_file, model_tags, model_description, package_description,
                     schema_file, dependencies, runtime, base_url, subscription, resource_group, host_account_name,
                     verb, context)


def _endpoint_create(package_id, endpoint_name, kube_config, acr_pull_secret, acs_master_url, acs_agent_url,
                     driver_file, model_id, model_name, model_file, model_tags, model_description, package_description,
                     schema_file, dependencies, runtime, base_url, subscription, resource_group, host_account_name,
                     verb, context):
    auth_token = get_host_account_token()
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(auth_token)}
    endpoint_url = MMS_ENDPOINT_URL.format(base_url, subscription, resource_group, host_account_name)

    with open(kube_config, 'r') as kube_config_file:
        kube_config_string = kube_config_file.read()

    if not package_id:
        package_create_success, package_id = _package_create(driver_file, model_id, model_name, model_file, model_tags,
                                                             model_description, package_description, schema_file,
                                                             dependencies, runtime, base_url, subscription,
                                                             resource_group, host_account_name, verb, context)
        if package_create_success is not SUCCESS_RETURN_CODE:
            return

    body = {'packageId': package_id, 'appName': endpoint_name, 'kubeConfig': kube_config_string,
            'acrImagePullSecret': acr_pull_secret, 'acsInfo': {'acsMasterUrl': acs_master_url,
                                                               'acsAgentUrl': acs_agent_url}}

    try:
        resp = context.http_call('post', endpoint_url, headers=headers, json=body)
    except requests.ConnectionError:
        print('Error connecting to {}.'.format(endpoint_url))
        return

    if resp.status_code != 202:
        print('Error occurred creating endpoint')
        print(resp.headers)
        print(resp.content)
        return

    operation_location = resp.headers['Operation-Location']
    create_operation_status_id = operation_location.split('/')[-1]

    operation_url = MMS_OPERATION_URL.format(base_url, subscription, resource_group, host_account_name, create_operation_status_id)
    operation_headers = {'Authorization': 'Bearer {}'.format(auth_token)}

    while True:
        try:
            operation_resp = context.http_call('get', operation_url, headers=operation_headers)
        except requests.ConnectionError:
            print('Error connecting to {}.'.format(operation_url))
            return

        if operation_resp.status_code == 200:
            resp_obj = get_json(operation_resp.content, pascal=True)
            operation_state = resp_obj['State']
            print(operation_state)

            if operation_state == 'NotStarted' or operation_state == 'Running':
                time.sleep(5)
            elif operation_state == 'Succeeded':
                endpoint_id = resp_obj['ResourceLocation'].split('/')[-1]
                print('Endpoint ID: {}'.format(endpoint_id))
                return SUCCESS_RETURN_CODE
            else:
                print(resp_obj)
                return
        else:
            print('Error occurred while polling for endpoint create operation')
            print(operation_resp.headers)
            print(operation_resp.content)
            return


def endpoint_show(endpoint_id, verb, context=cli_context):
    try:
        base_url, subscription, resource_group, host_account_name = get_sub_and_account_info()
    except CLIError as exc:
        raise exc

    _endpoint_show(endpoint_id, base_url, subscription, resource_group, host_account_name, verb, context)


def _endpoint_show(endpoint_id, base_url, subscription, resource_group, host_account_name, verb, context):
    auth_token = get_host_account_token()
    headers = {'Authorization': 'Bearer {}'.format(auth_token)}
    endpoint_url = MMS_ENDPOINT_URL.format(base_url, subscription, resource_group, host_account_name) + \
                   '/{}'.format(endpoint_id)

    try:
        resp = context.http_call('get', endpoint_url, headers=headers)
    except requests.ConnectionError:
        print('Error connecting to {}.'.format(endpoint_url))
        return

    if resp.status_code == 200:
        endpoint_obj = get_json(resp.content, pascal=True)
        print(endpoint_obj)
        return SUCCESS_RETURN_CODE
    else:
        print('Error occurred while attempting to show endpoint')
        print(resp.headers)
        print(resp.content)


def endpoint_list(verb, context=cli_context):
    try:
        base_url, subscription, resource_group, host_account_name = get_sub_and_account_info()
    except CLIError as exc:
        raise exc

    _endpoint_list(base_url, subscription, resource_group, host_account_name, verb, context)


def _endpoint_list(base_url, subscription, resource_group, host_account_name, verb, context):
    auth_token = get_host_account_token()
    headers = {'Authorization': 'Bearer {}'.format(auth_token)}
    endpoint_url = MMS_ENDPOINT_URL.format(base_url, subscription, resource_group, host_account_name)

    try:
        resp = context.http_call('get', endpoint_url, headers=headers)
    except requests.ConnectionError:
        print('Error connecting to {}'.format(endpoint_url))
        return

    if resp.status_code == 200:
        endpoints = get_json(resp.content, pascal=True)
        for endpoint in endpoints:
            print(endpoint)
        return SUCCESS_RETURN_CODE
    else:
        print('Error occurred while attempting to list endpoints')
        print(resp.headers)
        print(resp.content)


def endpoint_update():
    try:
        base_url, subscription, resource_group, host_account_name = get_sub_and_account_info()
    except CLIError as exc:
        raise exc

    _endpoint_update()


def _endpoint_update(verb, context):
    auth_token = get_host_account_token()
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(auth_token)}
    endpoint_url = MMS_ENDPOINT_URL.format(base_url, subscription, resource_group, host_account_name) + \
                   '/{}'.format(endpoint_id)

    if kube_config:
        with open(kube_config, 'r') as kube_config_file:
            kube_config_string = kube_config_file.read()

    if not package_id:
        package_create_success, package_id = _package_create(driver_file, model_id, model_name, model_file, model_tags,
                                                             model_description, package_description, schema_file,
                                                             dependencies, runtime, base_url, subscription,
                                                             resource_group, host_account_name, verb, context)
        if package_create_success is not SUCCESS_RETURN_CODE:
            return

    body = {'packageId': package_id, 'appName': endpoint_name, 'kubeConfig': kube_config_string,
            'acrImagePullSecret': acr_pull_secret, 'acsInfo': {'acsMasterUrl': acs_master_url,
                                                               'acsAgentUrl': acs_agent_url}}

    try:
        resp = context.http_call('put', endpoint_url, headers=headers, json=body)
    except requests.ConnectionError:
        print('Error connecting to {}.'.format(endpoint_url))
        return

    if resp.status_code != 202:
        print('Error occurred creating endpoint')
        print(resp.headers)
        print(resp.content)
        return

    operation_location = resp.headers['Operation-Location']
    create_operation_status_id = operation_location.split('/')[-1]

    operation_url = MMS_OPERATION_URL.format(base_url, subscription, resource_group, host_account_name, create_operation_status_id)
    operation_headers = {'Authorization': 'Bearer {}'.format(auth_token)}

    while True:
        try:
            operation_resp = context.http_call('get', operation_url, headers=operation_headers)
        except requests.ConnectionError:
            print('Error connecting to {}.'.format(operation_url))
            return

        if operation_resp.status_code == 200:
            resp_obj = get_json(operation_resp.content, pascal=True)
            operation_state = resp_obj['State']
            print(operation_state)

            if operation_state == 'NotStarted' or operation_state == 'Running':
                time.sleep(5)
            elif operation_state == 'Succeeded':
                endpoint_id = resp_obj['ResourceLocation'].split('/')[-1]
                print('Endpoint ID: {}'.format(endpoint_id))
                return SUCCESS_RETURN_CODE
            else:
                print(resp_obj)
                return
        else:
            print('Error occurred while polling for endpoint create operation')
            print(operation_resp.headers)
            print(operation_resp.content)
            return
    raise NotImplemented


def endpoint_delete(endpoint_id, verb, context=cli_context):
    try:
        base_url, subscription, resource_group, host_account_name = get_sub_and_account_info()
    except CLIError as exc:
        raise exc

    _endpoint_delete(endpoint_id, base_url, subscription, resource_group, host_account_name, verb, context)


def _endpoint_delete(endpoint_id, base_url, subscription, resource_group, host_account_name, verb, context):
    auth_token = get_host_account_token()
    headers = {'Authorization': 'Bearer {}'.format(auth_token)}
    endpoint_url = MMS_ENDPOINT_URL.format(base_url, subscription, resource_group, host_account_name) + \
                   '/{}'.format(endpoint_id)

    try:
        resp = context.http_call('delete', endpoint_url, headers=headers)
    except requests.ConnectionError:
        print('Error connecting to {}'.format(endpoint_url))
        return

    if resp.status_code == 200:
        print('Successfully deleted endpoing: {}'.format(endpoint_id))
        return SUCCESS_RETURN_CODE
    else:
        print('Error occurred while attempting to list endpoints')
        print(resp.headers)
        print(resp.content)
    raise NotImplemented
