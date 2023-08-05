# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.command import Command

import auth

__author__ = 'arun'


class Service_Account_Delete(Command):
    """
    Deletes a Service Account by its ID.
     Service Account once deleted cannot be reverted. Delete Status will be displayed as output
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Service_Account_Delete, self).get_parser(prog_name)
        parser.add_argument(
            'serviceaccount_id',
            metavar='<serviceaccount_id>',
            help='ID of the Service Account to be deleted',
        )
        return parser

    def take_action(self, parsed_args):
        response = auth.delete_service_account(parsed_args.serviceaccount_id)
        if response['status'] != 'success':
            raise Exception(response['message'])
