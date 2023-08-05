# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging


from cliff.show import ShowOne

import auth

__author__ = 'arun'


class RerunJob(ShowOne):
    """
    Re-run a Template Job by its ID.
     Template Job ID will be available as output when this command is executed
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(RerunJob, self).get_parser(prog_name)
        parser.add_argument(
            'job_id',
            metavar='<job_id>',
            help='ID of the Template Job to be reran',
        )
        parser.add_argument(
            'body',
            metavar='<body>',
            help='JSON content with the needed inputs to rerun the template',
        )

        return parser

    def take_action(self, parsed_args):
        job = auth.rerun_job(parsed_args.job_id, parsed_args.body)
        columns = ['Job_id']
        rows = [job.get('data').get('job_id')]
        return (columns, rows)
