# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.lister import Lister

import auth

__author__ = 'arun'


class Blueprints(Lister):
    """
    Retrieves a list of blueprints for a given tenant.
     Blueprints list can be filtered using scope, category etc., ID in the output is referred as Blueprint ID
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Blueprints, self).get_parser(prog_name)
        parser.add_argument(
            '--scope',
            metavar='<scope>',
            required=False,
            help='Blueprint Scope can be Global or Tenant',
        )

        parser.add_argument(
            '--category',
            metavar='<category>',
            required=False,
            help='Blueprint Category to be filtered',
        )

        parser.add_argument(
            '--limit',
            metavar='<limit>',
            required=False,
            help='Limits the number of blueprints that can be retrieved',
        )

        parser.add_argument(
            '--page_number',
            metavar='<page_number>',
            required=False,
            help='Page number of the blueprint list to be retrieved',
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
        blueprints = auth.list_blueprints(**url_params)
        columns = ('Id',
                   'Name',
                   'Scope',
                   'Resources',
                   'Status'
                   )
        rows = ((blueprint['id'], blueprint['name'], blueprint['scope'],
                blueprint['resources'], blueprint['status'])
                for blueprint in blueprints)
        return (columns, rows)
