#!/usr/bin/env python
# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

PROJECT = 'corestack'

# Change docs/sphinx/conf.py too!
VERSION = '0.2'

from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Corestack Command Line Interface',
    long_description=long_description,

    author='CoreStack',
    author_email='customer-success@cloudenablers.com',

    url='https://github.com/openstack/cliff',
    download_url='https://github.com/openstack/cliff/tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff', 'requests'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'corestack = corestack.main:main'
        ],
        'corestack': [
            'environment-create = corestack.create_environment:CreateEnvironment',
            'blueprint-execute = corestack.execute_blueprint:ExecuteBlueprint',
            'template-job-rerun = corestack.rerun_job:RerunJob',
            'schedule-create = corestack.create_schedule:CreateSchedule',
            'template-execute = corestack.execute_template:ExecuteTemplate',
            'script-execute = corestack.execute_script:ExecuteScript',
            'policy-execute = corestack.execute_policy:ExecutePolicy',
            'alarm-create = corestack.create_alarm:CreateAlarm',
            'inventory-create = corestack.create_inventory:CreateInventory',
            'environment-show = corestack.show_environment:ShowEnvironment',
            'environments-list = corestack.environments:Environments',
            'template-job-show = corestack.show_job:ShowJob',
            'template-jobs-list = corestack.jobs:Jobs',
            'inventory-show = corestack.show_inventory:ShowInventory',
            'inventories-list = corestack.inventories:Inventories',
            'policy-show = corestack.show_enginepolicy:ShowEnginePolicy',
            'policies-list = corestack.enginepolicies:Engine_Policies',
            'tenants-list = corestack.tenants:Tenants',
            'schedules-list = corestack.schedules:Schedules',
            'serviceaccount-show = corestack.show_serviceaccount:ShowServiceaccount',
            'alarm-show = corestack.show_alarm:ShowAlarm',
            'schedule-show = corestack.show_schedule:ShowSchedule',
            'templates-list = corestack.templates:Templates',
            'serviceaccounts-list = corestack.service_accounts:Service_Accounts',
            'alarms-list = corestack.alarms:Alarms',
            'template-show = corestack.show_template:ShowTemplate',
            'blueprint-show = corestack.show_blueprint:ShowBlueprint',
            'script-show = corestack.show_script:ShowScript',
            'scripts-list = corestack.scripts:Scripts',
            'blueprints-list = corestack.blueprints:Blueprints',
            'serviceaccount-delete = corestack.delete_service_account:Service_Account_Delete',
            'alarm-delete = corestack.delete_alarm:Alarm_Delete',
            'schedule-delete = corestack.delete_schedule:Schedule_Delete',
            'inventory-delete = corestack.delete_inventory:Inventory_Delete',
            'environment-delete = corestack.delete_environment:Environment_Delete',
        ],
    },

    zip_safe=False,
)
