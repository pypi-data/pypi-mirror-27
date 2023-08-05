# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging


from cliff.lister import Lister

import auth

__author__ = 'arun'


class Scripts(Lister):
    """
    Retrieves a list of CoreStack Scripts for a given tenant.
     List includes both Marketplace Scripts & My Scripts. Script list can be filtered using scope,
      category etc., ID in the output is referred as Script ID
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Scripts, self).get_parser(prog_name)
        parser.add_argument(
            '--scope',
            metavar='<scope>',
            required=False,
            help='Script Scope can be Global or Tenant',
        )
        parser.add_argument(
            '--category',
            metavar='<category>',
            required=False,
            help='Script Category to be filtered',
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            required=False,
            help='Number of Scirpt to be listed',
        )
        parser.add_argument(
            '--page',
            metavar='<page>',
            required=False,
            help='Page count of the Scirpt to be listed',
        )
        return parser

    def take_action(self, parsed_args):
        url_params = dict()
        if parsed_args.scope:
            url_params['scope'] = parsed_args.scope
        if parsed_args.category:
            url_params['category'] = parsed_args.category
        if parsed_args.limit:
            url_params['limit'] = parsed_args.limit
        if parsed_args.page:
            url_params['page'] = parsed_args.page
        scripts = auth.list_scripts(**url_params)
        columns = ('Id',
                   'Name',
                   'Config_type',
                   'Scope',
                   'Category',
                   'Created_at',
                   'Status'
                   )
        rows = ((script['id'], script['name'], script['config_type'], script['scope'],
                 ','.join(script['category']), script['created_at'],
                 script['status']) for script in scripts)
        return (columns, rows)
