# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.command import Command

import auth

__author__ = 'arun'


class Schedule_Delete(Command):
    """
    Deletes a schedule by its ID.
     Schedule ID can be fetched from the output of schedules-list command. Delete Status will be displayed as output
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Schedule_Delete, self).get_parser(prog_name)
        parser.add_argument(
            'schedule_id',
            metavar='<schedule_id>',
            help='ID of the CoreStack Schedule to be deleted',
        )
        return parser

    def take_action(self, parsed_args):
        response = auth.delete_schedule(parsed_args.schedule_id)
        if response['status'] != 'success':
            raise Exception(response['message'])
