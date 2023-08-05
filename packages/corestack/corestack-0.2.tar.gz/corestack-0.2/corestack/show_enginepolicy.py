# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging


from cliff.show import ShowOne

import auth

__author__ = 'arun'


class ShowEnginePolicy(ShowOne):
    """
    Retrieves a CoreStack Policy by its ID.
     Policy ID can be fetched from the output of policies-list command. Name, Description,
      Classification (Cost, Utilization, Security, Access etc.,),
       Created By, Updated By etc., will be available as output
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ShowEnginePolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy_id',
            metavar='<policy_id>',
            help='ID of the CoreStack Policy to be retrieved',
        )

        return parser

    def take_action(self, parsed_args):
        enginepolicy = auth.show_enginepolicy(parsed_args.policy_id)
        columns = ('Id',
                   'Name',
                   'Description',
                   'Services',
                   'Policytype',
                   'Classification',
                   'Created_by',
                   'Updated_by',
                   )
        rows = (enginepolicy.get('data').get('policies').get('id'), enginepolicy.get('data').get('policies').get('name'),
                enginepolicy.get('data').get('policies').get('description'),
                enginepolicy.get('data').get('policies').get('services'),
                enginepolicy.get('data').get('policies').get('policy_type'),
                enginepolicy.get('data').get('policies').get('classification'),
                enginepolicy.get('data').get('policies').get('created_by'),
                enginepolicy.get('data').get('policies').get('updated_by'))
        return (columns, rows)

