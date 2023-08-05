# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.show import ShowOne

import auth

__author__ = 'arun'


class CreateSchedule(ShowOne):
    """
    Creates a schedule in the given tenant.
     Templates, Scripts and Blueprint can be scheduled.
      Schedule can be recurring or per time execution as per the need. Schedule ID will be returned as output.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CreateSchedule, self).get_parser(prog_name)
        parser.add_argument(
            'body',
            metavar='<body>',
            help='JSON content with the needed inputs to create a schedule',
        )
        return parser

    def take_action(self, parsed_args):
        schedule = auth.create_schedule(parsed_args.body)
        columns = ['Id']
        rows = [schedule.get('data').get('schedule_id')]
        return (columns, rows)
