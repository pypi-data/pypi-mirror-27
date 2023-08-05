# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.command import Command

import auth

__author__ = 'arun'


class Environment_Delete(Command):
    """
    Deletes an Environment by its ID.
     Environment once deleted cannot be reverted. Delete Status will be displayed as output
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Environment_Delete, self).get_parser(prog_name)
        parser.add_argument(
            'environment_id',
            metavar='<environment_id>',
            help='ID of the Environment to be deleted',
        )
        return parser

    def take_action(self, parsed_args):
        response = auth.delete_environment(parsed_args.environment_id)
        if response['status'] != 'success':
            raise Exception(response['message'])
