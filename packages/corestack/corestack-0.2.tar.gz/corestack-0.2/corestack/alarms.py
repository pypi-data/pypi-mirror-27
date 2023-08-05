# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.lister import Lister

import auth

__author__ = 'arun'


class Alarms(Lister):
    """
    Retrieves a list of CoreStack Alarms for a given tenant.
     ID in the output is referred as Alarm ID
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        alarms = auth.list_alarms()
        columns = ('Id',
                   'Name',
                   'Status',
                   'Type',
                   'Updated_by',
                   'Created_by'
                   )
        rows = ((alarm['id'], alarm['name'], alarm['status'],
                alarm['type'], alarm['updated_by'],
                alarm['created_by']) for alarm in alarms)
        return (columns, rows)
