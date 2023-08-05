# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.show import ShowOne

import auth

__author__ = 'arun'


class ExecuteScript(ShowOne):
    """
    Executes a script by its ID with the inputs (Request Body).
     Request body is expected to vary for each script and the same can be identified using script
      content retrieved as part of script-show command
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ExecuteScript, self).get_parser(prog_name)
        parser.add_argument(
            'script_id',
            metavar='<script_id>',
            help='ID of the CoreStack Script to be executed',
        )
        parser.add_argument(
            'body',
            metavar='<body>',
            help='JSON content with the needed inputs to execute the script',
        )
        return parser

    def take_action(self, parsed_args):
        script = auth.execute_script(parsed_args.script_id, parsed_args.body)
        columns = ['Job Id']
        rows = [script.get('data').get('job_id')]
        return (columns, rows)
