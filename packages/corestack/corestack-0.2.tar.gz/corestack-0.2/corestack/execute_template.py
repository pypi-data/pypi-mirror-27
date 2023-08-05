# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.show import ShowOne

import auth

__author__ = 'arun'


class ExecuteTemplate(ShowOne):
    """
    Executes a template by its ID with the inputs (Request Body).
     Request body is expected to vary for each template and the same can be identified using template
      content retrieved as part of template-show command
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ExecuteTemplate, self).get_parser(prog_name)
        parser.add_argument(
            'template_id',
            metavar='<template_id>',
            help='ID of the CoreStack Template to be executed',
        )
        parser.add_argument(
            'body',
            metavar='<body>',
            help='JSON content with the needed inputs to execute the template',
        )
        return parser

    def take_action(self, parsed_args):
        template = auth.execute_template(parsed_args.template_id, parsed_args.body)
        columns = ['Job Id']
        rows = [template.get('data').get('job_id')]
        return (columns, rows)
