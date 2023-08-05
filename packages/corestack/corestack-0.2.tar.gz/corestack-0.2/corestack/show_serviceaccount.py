# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.show import ShowOne

import auth


class ShowServiceaccount(ShowOne):
    """
    Retrieves a Service Account by its ID.
     Service Account can be fetched from the output of serviceaccounts-list command. Name, Description, Created By,
      Updated By etc., will be available as output
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ShowServiceaccount, self).get_parser(prog_name)
        parser.add_argument(
            'serviceaccount_id',
            metavar='<serviceaccount_id>',
            help='ID of the Service Account to be retrieved',
        )

        return parser

    def take_action(self, parsed_args):
        service_account = auth.show_serviceaccount(parsed_args.serviceaccount_id)
        columns = ('Id',
                   'Name',
                   'Description',
                   'Service_type',
                   'Service_id',
                   'Resource_listing_support',
                   'Created_by',
                   'Updated_by',
                   )
        rows = (service_account.get('data').get('id'), service_account.get('data').get('name'),
                service_account.get('data').get('description'), service_account.get('data').get('service_type'),
                service_account.get('data').get('service_id'),
                service_account.get('data').get('resource_listing_support'),
                service_account.get('data').get('created_by'), service_account.get('data').get('updated_by'))
        return (columns, rows)
