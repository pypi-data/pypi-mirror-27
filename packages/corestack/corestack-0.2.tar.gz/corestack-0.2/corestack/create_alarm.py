# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.show import ShowOne

import auth

__author__ = 'arun'


class CreateAlarm(ShowOne):
    """
    Create an alarm with the inputs (Request Body).
     Alarm ID will be returned as output
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CreateAlarm, self).get_parser(prog_name)
        parser.add_argument(
            'body',
            metavar='<body>',
            help='JSON content with the needed inputs to create an alarm',
        )
        return parser

    def take_action(self, parsed_args):
        alarm = auth.create_alarm(parsed_args.body)
        columns = ['Id', 'Name', 'Status']
        rows = [alarm.get('data').get('id'), alarm.get('data').get('name'), alarm.get('data').get('status')]
        return (columns, rows)
