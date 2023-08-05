# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging


from cliff.show import ShowOne

import auth

__author__ = 'arun'


class ShowBlueprint(ShowOne):
    """
    Retrieves a CoreStack Blueprint by its ID.
     Blueprint ID can be fetched from the output of blueprints-list command.
      Name, Scope, Execution Type (On-demand or Scheduled), Created By, Updated By etc., will be available as output
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ShowBlueprint, self).get_parser(prog_name)
        parser.add_argument(
                'blueprint_id',
                metavar='<blueprint_id>',
                help='ID of the CoreStack Blueprint to be retrieved',
        )

        return parser

    def take_action(self, parsed_args):
        blueprint = auth.show_blueprint(parsed_args.blueprint_id)
        columns = ('Id',
                   'Name',
                   'Scope',
                   'Blueprint_type',
                   'Execution_type',
                   'Status',
                   'Is_deleted',
                   'Created_by',
                   'Updated_by',
                   )
        rows = (blueprint.get('data').get('id'), blueprint.get('data').get('name'), blueprint.get('data').get('scope'),
                blueprint.get('data').get('resources')[0].get('type'),blueprint.get('data').get('resources')[0].
                get('execution_type'), blueprint.get('data').get('status'), blueprint.get('data').get('is_deleted'),
                blueprint.get('data').get('created_by'), blueprint.get('data').get('updated_by'))
        return (columns, rows)
