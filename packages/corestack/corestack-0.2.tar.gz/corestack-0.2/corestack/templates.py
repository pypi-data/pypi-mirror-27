# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.lister import Lister

import auth


class Templates(Lister):
    """
    Retrieves a list of CoreStack templates for a given tenant.
     List includes both Marketplace templates & My templates.
      Template list can be filtered using Scope and Category.
       ID in the output is referred as Template ID
    """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Templates, self).get_parser(prog_name)
        parser.add_argument(
            '--scope',
            metavar='<scope>',
            required=False,
            help='Template Scope can be Global or Tenant',
        )

        parser.add_argument(
            '--category',
            metavar='<category>',
            required=False,
            help='Template Category to be filtered',
        )

        parser.add_argument(
            '--limit',
            metavar='<limit>',
            required=False,
            help='Limits the number of templates that can be retrieved',
        )

        parser.add_argument(
            '--page_number',
            metavar='<page_number>',
            required=False,
            help='Page number of the templates list to be retrieved',
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
        templates = auth.list_templates(**url_params)
        columns = ('Id',
                   'Name',
                   'Scope',
                   'Engine_type',
                   'Type',
                   'Classification'
                   )
        rows = ((template['id'], template['name'], template['scope'],
                template['engine_type'], ','.join(template['type']),
                ','.join(template['classification'])) for template in templates)
        return (columns, rows)
