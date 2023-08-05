# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.show import ShowOne

import auth

__author__ = 'arun'


class CreateEnvironment(ShowOne):
    """
    Creates an environment in the given tenant.
     Environment ID will be returned as output.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CreateEnvironment, self).get_parser(prog_name)
        parser.add_argument(
            'body',
            metavar='<body>',
            help='JSON content with the needed inputs to create an environment',
        )
        return parser

    def take_action(self, parsed_args):
        environment = auth.create_environment(parsed_args.body)
        columns = ['Id']
        rows = [environment.get('data').get('id')]
        return (columns, rows)
