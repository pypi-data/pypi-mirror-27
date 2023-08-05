# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging


from cliff.lister import Lister

import auth

__author__ = 'arun'


class Engine_Policies(Lister):
    """
    Retrieves a list of CoreStack Policies for a given tenant.
     ID in the output is referred as Policy ID
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Engine_Policies, self).get_parser(prog_name)
        parser.add_argument(
            '--scope',
            metavar='<scope>',
            required=False,
            help='Policy Scope can be Global or Tenant',
        )

        parser.add_argument(
            '--category',
            metavar='<category>',
            required=False,
            help='Policy Category to be filtered',
        )

        parser.add_argument(
            '--limit',
            metavar='<limit>',
            required=False,
            help='Limits the number of Policies that can be retrieved',
        )

        parser.add_argument(
            '--page_number',
            metavar='<page_number>',
            required=False,
            help='Page number of the Policies list to be retrieved',
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
        if parsed_args.page_number:
            url_params['page'] = parsed_args.page_number

        engine_policies = auth.list_engine_policies(**url_params)
        columns = ('Id',
                   'Name',
                   'Status',
                   'Updated_by',
                   'Created_by'
                   )
        rows = ((engine_policy['id'], engine_policy['name'], engine_policy['status'],
                 engine_policy['updated_by'], engine_policy['created_by']) for engine_policy in engine_policies)
        return (columns, rows)
