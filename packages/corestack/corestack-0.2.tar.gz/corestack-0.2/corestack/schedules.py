# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging


from cliff.lister import Lister

import auth

__author__ = 'arun'


class Schedules(Lister):
    """
    Retrieves a list of Schedules for a given tenant.
     List contains schedules of templates and scripts. ID in the output is referred as Schedule ID
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        list_schedules = auth.list_schedules()
        columns = ('Id',
                   'Name',
                   'Status',
                   'Description',
                   'Created_at'
                   )
        rows = ((list_schedule['id'], list_schedule['name'], list_schedule['status'],
                list_schedule['description'], list_schedule['created_at']) for list_schedule in list_schedules)
        return (columns, rows)
