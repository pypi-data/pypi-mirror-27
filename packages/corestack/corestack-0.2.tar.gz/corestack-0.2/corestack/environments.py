# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.lister import Lister

import auth

__author__ = 'arun'


class Environments(Lister):
    """
    Retrieves a list of environments for a given tenant.
     ID in the output is referred as Environment ID
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        environments = auth.list_environments()
        columns = ('Id',
                   'Name',
                   'Environment_type',
                   'Metadata',
                   'Description',
                   'Created_by'
                   )
        rows = ((environment['id'], environment['name'], environment['environment_type'],
                environment['metadata'], environment['description'],
                environment['created_by']) for environment in environments)
        return (columns, rows)
