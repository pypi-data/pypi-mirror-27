# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.show import ShowOne

import auth

__author__ = 'arun'


class ShowAlarm(ShowOne):
    """
    Retrieves a CoreStack Alarm by its ID.
     Alarm ID can be fetched from the output of alarms-list command. Name, Status,
      Created By, Updated By etc., will be available as output
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ShowAlarm, self).get_parser(prog_name)
        parser.add_argument(
            'alarm_id',
            metavar='<alarm_id>',
            help='ID of the CoreStack Alarm to be retrieved',
        )

        return parser

    def take_action(self, parsed_args):
        alarm = auth.show_alarm(parsed_args.alarm_id)
        columns = ('Id',
                   'Name',
                   'Alarm_action_type',
                   'Status',
                   'Project_name',
                   'Type',
                   'Created_by',
                   'Updated_by',
                   )
        rows = (alarm.get('data').get('id'), alarm.get('data').get('name'), alarm.get('data').get('alarm_action_type'),
                alarm.get('data').get('status'), alarm.get('data').get('project_name'),
                alarm.get('data').get('type'), alarm.get('data').get('created_by'), alarm.get('data').get('updated_by'))
        return (columns, rows)
