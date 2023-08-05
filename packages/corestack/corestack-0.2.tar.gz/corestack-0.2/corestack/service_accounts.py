# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.lister import Lister

import auth

__author__ = 'arun'


class Service_Accounts(Lister):
    """
    Retrieves a list of Service Accounts for a given tenant.
     Service Accounts can be of cloud services in AWS, Azure, OpenStack etc.,
      ID in the output is referred as Service Account ID
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        service_accounts = auth.list_service_accounts()
        columns = ('Id',
                   'Name',
                   'Status',
                   'Service_Name',
                   'Service_Type',
                   'Created_by'
                   )
        rows = ((service_acc['id'], service_acc['name'], service_acc['status'],
                service_acc['service_name'], service_acc['service_type'],
                service_acc['created_by']) for service_acc in service_accounts)
        return(columns, rows)
