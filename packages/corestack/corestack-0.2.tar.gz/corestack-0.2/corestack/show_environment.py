# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.show import ShowOne

import auth

__author__ = 'arun'


class ShowEnvironment(ShowOne):
    """
    Retrieves an Environment by its ID.
     Environment ID can be fetched from the output of environments-list command.
      Name, Type, Created By and Updated At etc., will be available as output
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ShowEnvironment, self).get_parser(prog_name)
        parser.add_argument(
            'environment_id',
            metavar='<environment_id>',
            help='ID of the Environment to be retrieved',
        )

        return parser

    def take_action(self, parsed_args):
        environment = auth.show_environment(parsed_args.environment_id)
        columns = ('Id',
                   'Name',
                   'Environment_type',
                   'Created_by',
                   'Created_at',
                   'Updated_by',
                   'Updated_at',
                   )
        rows = (environment.get('data').get('id'), environment.get('data').get('name'),
                environment.get('data').get('environment_type'), environment.get('data').get('created_by'), environment.get('data').get('created_at'),
                environment.get('data').get('updated_by'), environment.get('data').get('updated_at'))
        return (columns, rows)
