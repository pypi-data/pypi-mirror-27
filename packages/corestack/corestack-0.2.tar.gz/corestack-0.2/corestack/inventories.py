# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging


from cliff.lister import Lister

import auth

__author__ = 'arun'


class Inventories(Lister):
    """
    Retrieves a list of inventories for a given tenant.
     ID in the output is referred as Inventory ID
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Inventories, self).get_parser(prog_name)
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            required=False,
            help='Limits the number of inventories that can be retrieved',
        )

        parser.add_argument(
            '--page_number',
            metavar='<page_number>',
            required=False,
            help='Page number of the inventories list to be retrieved',
        )

        return parser

    def take_action(self, parsed_args):
        url_params = dict()
        if parsed_args.limit:
            url_params['limit'] = parsed_args.limit
        if parsed_args.page_number:
            url_params['page'] = parsed_args.page_number
        inventories = auth.list_inventories(**url_params)
        columns = ('Id',
                   'Name',
                   'Resource_name',
                   'Resource_type',
                   'Description',
                   'Created_by'
                   )
        rows = ((inventory['id'], inventory['name'], inventory['resource_name'],
                inventory['resource_type'], inventory['description'],
                inventory['created_by']) for inventory in inventories)
        return (columns, rows)
