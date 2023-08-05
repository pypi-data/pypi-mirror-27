# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.show import ShowOne

import auth

__author__ = 'arun'


class ExecutePolicy(ShowOne):
    """
    Executes a policy by its ID with the inputs (Request Body).
     Request body is expected to vary for each policy and the same can be identified using policy content retrieved as part of policy-show command
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ExecutePolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy_id',
            metavar='<policy_id>',
            help='ID of the CoreStack Policy to be executed',
        )
        parser.add_argument(
            'body',
            metavar='<body>',
            help='JSON content with the needed inputs to execute a policy',
        )
        return parser

    def take_action(self, parsed_args):
        policy = auth.execute_policy(parsed_args.policy_id, parsed_args.body)
        columns = ['Job id']
        rows = [policy.get('job_id')]
        return (columns, rows)
