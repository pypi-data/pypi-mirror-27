# Copyright (c) 2017, Cloudenablers Inc
# All rights reserved.

import logging

from cliff.show import ShowOne

import auth


class ShowTemplate(ShowOne):
    """
    Retrieves a CoreStack template by its ID.
     Template ID can be fetched from the output of templates-list command. Name, Description, Template content,
      Engine Type (Heat, Mistral, ARM etc.,), Created By, Updated By etc., will be available as output
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ShowTemplate, self).get_parser(prog_name)
        parser.add_argument(
            'template_id',
            metavar='<template_id>',
            help='ID of the CoreStack Template to be retrieved',
        )
        return parser

    def take_action(self, parsed_args):
        template = auth.show_template(parsed_args.template_id)
        columns = ('Id',
                   'Name',
                   'Description',
                   'Scope',
                   'Engine_type',
                   'Type',
                   'Services',
                   'Resources',
                   'Content',
                   'Created_by',
                   'Updated_by',
                   )
        rows = (template.get('data').get('id'), template.get('data').get('name'),
                template.get('data').get('description'),
                template.get('data').get('scope'), template.get('data').get('engine_type'),
                ','.join(template.get('data').get('type')), ','.join(template.get('data').get('services')),
                ','.join(template.get('data').get('resources')), str(template.get('data').get('content')),
                template.get('data').get('created_by'), template.get('data').get('updated_by'))
        return(columns, rows)

