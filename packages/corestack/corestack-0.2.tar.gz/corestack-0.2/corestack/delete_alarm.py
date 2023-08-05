# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.command import Command

import auth

__author__ = 'arun'


class Alarm_Delete(Command):
    """
    Deletes an Alarm by its ID.
     Alarm once deleted cannot be reverted. Delete Status will be displayed as output
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Alarm_Delete, self).get_parser(prog_name)
        parser.add_argument(
            'alarm_id',
            metavar='<alarm_id>',
            help='ID of the CoreStack Alarm to be deleted',
        )
        return parser

    def take_action(self, parsed_args):
        response = auth.delete_alarm(parsed_args.alarm_id)
        if response['status'] != 'success':
            raise Exception(response['message'])
