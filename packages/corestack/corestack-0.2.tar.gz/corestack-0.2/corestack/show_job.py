# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.show import ShowOne

import auth

__author__ = 'arun'


class ShowJob(ShowOne):
    """
    Retrieves a Template Job by its ID.
     Template Job ID can be fetched from the output of jobs-list command.
      Job Created Time, Status etc., will be available as output
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ShowJob, self).get_parser(prog_name)
        parser.add_argument(
            'job_id',
            metavar='<job_id>',
            help='ID of the Template Job to be retrieved',
        )

        return parser

    def take_action(self, parsed_args):
        job = auth.show_job(parsed_args.job_id)
        columns = ('Id',
                   'Name',
                   'Status',
                   'Is_resource_active',
                   'Template_id',
                   'Template_category',
                   'Service_accounts',
                   'Completed_at',
                   'Created_at',
                   'User_name',
                   )
        rows = (job.get('data').get('id'), job.get('data').get('name'), job.get('data').get('status'),
                job.get('data').get('is_resource_active'), job.get('data').get('template_id'),
                job.get('data').get('template_category'),
                ','.join([service_account['name'] for service_account in job.get('data').get('service_accounts')]),
                job.get('data').get('completed_at'), job.get('data').get('created_at'),
                job.get('data').get('user_name'))
        return (columns, rows)
