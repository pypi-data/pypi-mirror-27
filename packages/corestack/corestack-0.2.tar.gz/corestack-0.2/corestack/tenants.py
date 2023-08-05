# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.lister import Lister

import auth


class Tenants(Lister):
    """
    Retrieves a list of CoreStack Tenants that the specified user has access to.
     ID in the output is referred as Tenant ID.
      Tenant ID should be specified in the openrc file for the rest of CoreStack CLI commands to work.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Tenants, self).get_parser(prog_name)
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            required=False,
            help='Limits the number of tenants that can be retrieved',
        )

        parser.add_argument(
            '--page_number',
            metavar='<page_number>',
            required=False,
            help='Page number of the tenants list to be retrieved',
        )

        return parser

    def take_action(self, parsed_args):
        url_params = dict()
        if parsed_args.limit:
            url_params['limit'] = parsed_args.limit
        if parsed_args.page_number:
            url_params['page'] = parsed_args.page_number

        tenants = auth.list_tenants(**url_params)
        columns = ('Id',
                   'Tenant name',
                   'Status',
                   )
        rows = ((tenant['id'], tenant['name'], tenant['status']) for tenant in tenants)
        return (columns, rows)
