# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.show import ShowOne

import auth

__author__ = 'arun'


class ExecuteBlueprint(ShowOne):
    """
    Executes a blueprint by its ID with the inputs (Request Body).
     Request body is expected to vary for each blueprint and the same can be identified using blueprint
      content retrieved as part of blueprint-show command
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ExecuteBlueprint, self).get_parser(prog_name)
        parser.add_argument(
            'blueprint_id',
            metavar='<blueprint_id>',
            help='ID of the CoreStack Blueprint to be executed',
        )
        parser.add_argument(
            'body',
            metavar='<body>',
            help='JSON content with the needed inputs to execute a blueprint',
        )

        return parser

    def take_action(self, parsed_args):
        blueprint = auth.execute_blueprint(parsed_args.blueprint_id, parsed_args.body)
        columns = ['Job Id']
        rows = [blueprint.get('data').get('job_id')]
        return (columns, rows)
