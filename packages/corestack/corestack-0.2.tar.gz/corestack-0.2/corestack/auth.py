# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import requests
import json
import os

endpoint = os.environ.get('CORESTACK_ENDPOINT')
username = os.environ.get('CORESTACK_USERNAME')
password = os.environ.get('CORESTACK_PASSWORD')
tenant_id = os.environ.get('CORESTACK_TENANT_ID')


def login():
    url = "%s/v1/auth/tokens" % endpoint
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    body = json.dumps({"username": username, "password": password})
    response = requests.post(url, data=body, headers=headers).json()
    if response["status"] == "success":
        return response['data']['token']['key']
    else:
        raise Exception(response["message"])


def list_tenants(**kwargs):
    params = ''
    for key, value in kwargs.items():
        params = params + '%s=%s&' % (key, value)
    url = "%s/v1/projects?%s" % (endpoint, params)
    token = login()
    headers = {"X-Auth-User": username, "X-Auth-Token": token}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response['data']['projects']
    else:
        raise Exception(response["message"])


def list_templates(**kwargs):
    params = ''
    for key, value in kwargs.items():
        params = params + '%s=%s&' % (key, value)
    url = "%s/v1/%s/templates?%s" % (endpoint, tenant_id, params)
    token = login()
    headers = {"X-Auth-User": username, "X-Auth-Token": token}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response['data']['templates']
    else:
        raise Exception(response["message"])


def list_blueprints(**kwargs):
    params = ''
    for key, value in kwargs.items():
        params = params + '%s=%s&' % (key, value)
    url = "%s/v1/%s/blueprints?%s" % (endpoint, tenant_id, params)
    token = login()
    headers = {"X-Auth-User": username, "X-Auth-Token": token}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response['data']['blueprints']
    else:
        raise Exception(response["message"])


def list_scripts(**kwargs):
    params = ''
    for key, value in kwargs.items():
        params = params + '%s=%s&' % (key, value)
    url = "%s/v1/%s/scripts?%s" % (endpoint, tenant_id, params)
    token = login()
    headers = {"X-Auth-User": username, "X-Auth-Token": token}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response['data']['scripts']
    else:
        raise Exception(response["message"])


def list_service_accounts():
    url = "%s/v1/%s/serviceaccounts" % (endpoint, tenant_id)
    token = login()
    headers = {"X-Auth-User": username, "X-Auth-Token": token}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response['data']
    else:
        raise Exception(response["message"])


def list_engine_policies(**kwargs):
    params = ''
    for key, value in kwargs.items():
        params = params + '%s=%s&' % (key, value)
    url = "%s/v1/%s/policies?%s" % (endpoint, tenant_id, params)
    token = login()
    headers = {"X-Auth-User": username, "X-Auth-Token": token}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response['data']['policies']
    else:
        raise Exception(response["message"])


def list_inventories(**kwargs):
    params = ''
    for key, value in kwargs.items():
        params = params + '%s=%s&' % (key, value)
    url = "%s/v1/%s/resourceelements?%s" % (endpoint, tenant_id, params)
    token = login()
    headers = {"X-Auth-User": username, "X-Auth-Token": token}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response['data']['inventories']
    else:
        raise Exception(response["message"])


def list_environments():
    url = "%s/v1/%s/environments" % (endpoint, tenant_id)
    token = login()
    headers = {"X-Auth-User": username, "X-Auth-Token": token}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response['data']
    else:
        raise Exception(response["message"])


def list_jobs(**kwargs):
    params = ''
    for key, value in kwargs.items():
        params = params + '%s=%s&' % (key, value)
    url = "%s/v1/%s/jobs?%s" % (endpoint, tenant_id, params)
    token = login()
    headers = {"X-Auth-User": username, "X-Auth-Token": token}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response['data']['jobs']
    else:
        raise Exception(response["message"])


def list_alarms():
    url = "%s/v1/%s/alarms" % (endpoint, tenant_id)
    token = login()
    headers = {"X-Auth-User": username, "X-Auth-Token": token}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response['data']['alarms']
    else:
        raise Exception(response["message"])


def list_schedules():
    url = "%s/v1/%s/schedules" % (endpoint, tenant_id)
    token = login()
    headers = {"X-Auth-User": username, "X-Auth-Token": token}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response['data']['schedules']
    else:
        raise Exception(response["message"])


def show_template(template_id):
    url = "%s/v1/%s/templates/%s" % (endpoint, tenant_id, template_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def create_alarm(body):
    url = "%s/v1/%s/alarms" % (endpoint, tenant_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.post(url, body, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def create_inventory(body):
    url = "%s/v1/%s/resourceelements" % (endpoint, tenant_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.post(url, body, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def create_schedule(body):
    url = "%s/v1/%s/schedules" % (endpoint, tenant_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.post(url, body, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def create_environment(body):
    url = "%s/v1/%s/environments" % (endpoint, tenant_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.post(url, body, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def execute_template(template_id, body):
    url = "%s/v1/%s/templates/%s/execute" % (endpoint, tenant_id, template_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.post(url, body, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def execute_script(script_id, body):
    url = "%s/v1/%s/scripts/%s?action=execute" % (endpoint, tenant_id, script_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.post(url, body, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def execute_blueprint(blueprint_id, body):
    url = "%s/v1/%s/blueprints/%s/execute" % (endpoint, tenant_id, blueprint_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.post(url, body, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def rerun_job(job_id, body):
    url = "%s/v1/%s/jobs/%s?action=rerun" % (endpoint, tenant_id, job_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.put(url, body, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def execute_policy(policy_id, body):
    url = "%s/v1/%s/policies/%s/execute" % (endpoint, tenant_id, policy_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.post(url, body, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def show_serviceaccount(serviceaccount_id):
    url = "%s/v1/%s/serviceaccounts/%s" % (endpoint, tenant_id, serviceaccount_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def show_environment(environment_id):
    url = "%s/v1/%s/environments/%s" % (endpoint, tenant_id, environment_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def show_enginepolicy(policy_id):
    url = "%s/v1/%s/policies/%s" % (endpoint, tenant_id, policy_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def show_inventory(inventory_id):
    url = "%s/v1/%s/resourceelements/%s" % (endpoint, tenant_id, inventory_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def show_blueprint(blueprint_id):
    url = "%s/v1/%s/blueprints/%s" % (endpoint, tenant_id, blueprint_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def show_schedule(schedule_id):
    url = "%s/v1/%s/schedules/%s" % (endpoint, tenant_id, schedule_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def show_alarm(alarm_id):
    url = "%s/v1/%s/alarms/%s" % (endpoint, tenant_id, alarm_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def show_job(job_id):
    url = "%s/v1/%s/jobs/%s" % (endpoint, tenant_id, job_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def show_script(script_id):
    url = "%s/v1/%s/scripts/%s" % (endpoint, tenant_id, script_id)
    headers = {"X-Auth-User": username, "X-Auth-Token": login()}
    response = requests.get(url, headers=headers).json()
    if response["status"] == "success":
        return response
    else:
        raise Exception(response["message"])


def delete_service_account(service_account_id):
    url = "%s/v1/%s/serviceaccounts/%s" % (endpoint, tenant_id, service_account_id)
    token = login()
    headers = {"X-Auth-User": username, "X-Auth-Token": token}
    response = requests.delete(url, headers=headers).json()
    return response


def delete_environment(environment_id):
    url = "%s/v1/%s/environments/%s" % (endpoint, tenant_id, environment_id)
    token = login()
    headers = {"X-Auth-User": username, "X-Auth-Token": token}
    response = requests.delete(url, headers=headers).json()
    return response


def delete_inventory(inventory_id):
    url = "%s/v1/%s/resourceelements/%s" % (endpoint, tenant_id, inventory_id)
    token = login()
    headers = {"X-Auth-User": username, "X-Auth-Token": token}
    response = requests.delete(url, headers=headers).json()
    return response


def delete_alarm(alarm_id):
    url = "%s/v1/%s/alarms/%s" % (endpoint, tenant_id, alarm_id)
    token = login()
    headers = {"X-Auth-User": username, "X-Auth-Token": token}
    response = requests.delete(url, headers=headers).json()
    return response


def delete_schedule(schedule_id):
    url = "%s/v1/%s/schedules/%s" % (endpoint, tenant_id, schedule_id)
    token = login()
    headers = {"X-Auth-User": username, "X-Auth-Token": token}
    response = requests.delete(url, headers=headers).json()
    return response
