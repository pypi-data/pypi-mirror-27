# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging
import json


from cliff.show import ShowOne

import auth

__author__ = 'arun'


class ShowSchedule(ShowOne):
    """
    Retrieves a schedule by its ID.
     Schedule ID can be fetched from the output of schedules-list command.
      Name, Schedule, Arguments involved in the execution, Created By etc., will be available as output
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ShowSchedule, self).get_parser(prog_name)
        parser.add_argument(
            'schedule_id',
            metavar='<schedule_id>',
            help='ID of the CoreStack Schedule to be retrieved',
        )

        return parser

    def take_action(self, parsed_args):
        schedule = auth.show_schedule(parsed_args.schedule_id)
        columns = ('Id',
                   'Name',
                   'Type',
                   'Timeout',
                   'Schedule',
                   'Args',
                   'Created_by',
                   'Updated_by',
                   )
        rows = (schedule.get('data').get('id'), schedule.get('data').get('name'),
                schedule.get('data').get('type'), schedule.get('data').get('timeout'),
                json.dumps(schedule.get('data').get('schedule')), json.dumps(schedule.get('data').get('args')),
                schedule.get('data').get('created_by'), schedule.get('data').get('updated_by'))
        return (columns, rows)
