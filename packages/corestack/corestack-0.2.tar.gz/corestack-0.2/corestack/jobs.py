# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.lister import Lister

import auth

__author__ = 'arun'


class Jobs(Lister):
    """
    Retrieves a list of template jobs for a given tenant.
     ID in the output is referred as Template Job ID
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Jobs, self).get_parser(prog_name)
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            required=False,
            help='Limits the number of template jobs that can be retrieved',
        )

        parser.add_argument(
            '--page_number',
            metavar='<page_number>',
            required=False,
            help='Page number of the template jobs list to be retrieved',
        )

        return parser

    def take_action(self, parsed_args):
        url_params = dict()
        if parsed_args.limit:
            url_params['limit'] = parsed_args.limit
        if parsed_args.page_number:
            url_params['page'] = parsed_args.page_number
        jobs = auth.list_jobs(**url_params)
        columns = ('Id',
                   'Name',
                   'Status',
                   'Type',
                   'Template_name',
                   'Created_at',
                   'Service_accounts',
                   'User_name',
                   'Resource_elements'
                   )
        rows = ((job['id'], job['name'], job['status'],
                job['type'], job['template_name'],
                job['created_at'], ','.join([service_account['name'] for service_account in job['service_accounts']]), job['user_name'],
                job['resource_elements']) for job in jobs)
        return (columns, rows)
