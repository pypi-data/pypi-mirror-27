from django.core.management.base import BaseCommand, CommandError

import opbeat_django.api
import opbeat_django.conf


class Command(BaseCommand):
    help = 'Notifies Opbeat of a new release being deployed'
    arguments = (
        (
            ('-r', '--revision'),
            {
                'default': None, 'dest': 'rev',
                'help': 'Revision (usually commit hash).',
            },
        ),
        (
            ('-b', '--branch'),
            {
                'default': None, 'dest': 'branch',
                'help': 'Branch (optional).',
            },
        ),
        (
            ('-m', '--machine'),
            {
                'default': None, 'dest': 'machine',
                'help': 'Machine (optional).',
            },
        ),
        (
            ('-o', '--organization-id'),
            {
                'default': None, 'dest': 'org_id',
                'help': 'Opbeat organization ID (overrides settings and env).',
            },
        ),
        (
            ('-a', '--app-id'),
            {
                'default': None, 'dest': 'app_id',
                'help': 'Opbeat app ID (overrides settings and env).',
            },
        ),
        (
            ('-t', '--token'),
            {
                'default': None, 'dest': 'token',
                'help': 'Opbeat secret token (overrides settings and env).',
            },
        ),
    )

    def add_arguments(self, parser):
        for args, kwargs in self.arguments:
            parser.add_argument(*args, **kwargs)

    def handle(self, *args, **options):
        # TODO: move this code to some function so it can be reused
        config = {}
        revision = {
            'rev': opbeat_django.conf.REV,
            'branch': opbeat_django.conf.BRANCH,
            'machine': opbeat_django.conf.MACHINE,
        }
        # FIXME: in one case we set defaults from conf in another we don't
        for key in ('org_id', 'app_id', 'token'):
            if options.get(key):
                config[key] = options[key]
        for key in ('rev', 'branch', 'machine'):
            if options.get(key):
                revision[key] = options[key]
            if not revision.get(key):
                del revision[key]  # remove nones so they don't mess with data
        if not revision.get('rev'):
            raise CommandError('Revision is not set')
        # TODO: warning if branch is missing?
        if revision.get('machine'):
            revision['status'] = 'machine-completed'
        else:
            revision['status'] = 'completed'

        client = opbeat_django.api.OpbeatAPI(**config)
        client.release(**revision)
