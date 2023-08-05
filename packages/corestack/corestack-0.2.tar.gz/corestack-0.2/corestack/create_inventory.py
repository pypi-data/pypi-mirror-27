# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.show import ShowOne

import auth

__author__ = 'arun'


class CreateInventory(ShowOne):
    """
    Creates an inventory in the given tenant.
     Inventory ID will be returned as output.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CreateInventory, self).get_parser(prog_name)
        parser.add_argument(
            'body',
            metavar='<body>',
            help='JSON content with the needed inputs to create an inventory',
        )
        return parser

    def take_action(self, parsed_args):
        inventory = auth.create_inventory(parsed_args.body)
        columns = ['Id']
        rows = [inventory.get('data').get('id')]
        return (columns, rows)
