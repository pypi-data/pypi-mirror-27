# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging


from cliff.show import ShowOne

import auth

__author__ = 'arun'


class ShowInventory(ShowOne):
    """
    Retrieves a Inventory by its ID.
     Inventory ID can be fetched from the output of inventories-list command.
      Name, Resource Name, Resource Type, Created At etc., will be available as output
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ShowInventory, self).get_parser(prog_name)
        parser.add_argument(
            'inventory_id',
            metavar='<inventory_id>',
            help='ID of the CoreStack Inventory to be retrieved',
        )

        return parser

    def take_action(self, parsed_args):
        inventory = auth.show_inventory(parsed_args.inventory_id)
        columns = ('Id',
                   'Name',
                   'Resource_name',
                   'Resource_type',
                   'Status',
                   'Created_at',
                   'Resource_listing_support',
                   )
        rows = (inventory.get('data').get('id'), inventory.get('data').get('name'),
                inventory.get('data').get('resource_name'), inventory.get('data').get('resource_type'), inventory.get('data').get('status'),
                inventory.get('data').get('created_at'), inventory.get('data').get('resource_listing_support'))
        return (columns, rows)

