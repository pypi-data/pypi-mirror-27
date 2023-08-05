# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.show import ShowOne

import auth

__author__ = 'arun'


class ShowScript(ShowOne):
    """
    Retrieves a CoreStack Script by its ID.
     Script ID can be fetched from the output of scripts-list command.
      Name, Description, Config Type (Shell, Ansible, Chef etc.,),
       Created By, Updated By etc., will be available as output
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ShowScript, self).get_parser(prog_name)
        parser.add_argument(
            'script_id',
            metavar='<script_id>',
            help='ID of the CoreStack Script to be retrieved',
        )

        return parser

    def take_action(self, parsed_args):
        script = auth.show_script(parsed_args.template)
        columns = ('Id',
                   'Name',
                   'Description',
                   'Scope',
                   'Config_type',
                   'Config_version',
                   'File_authentication',
                   'Created_by',
                   'Updated_by',
                   )
        rows = (script.get('data').get('id'), script.get('data').get('name'), script.get('data').get('description'),
                script.get('data').get('scope'), script.get('data').get('config_type'),
                script.get('data').get('config_version'), str(script.get('data').get('file_authentication')),
                script.get('data').get('created_by'), script.get('data').get('updated_by'))
        return (columns, rows)
