# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Red Hat
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#
import json
import sys

from pdc_client.plugin_helpers import PDCClientPlugin, get_paged, add_parser_arguments, extract_arguments


class GlobalComponentPlugin(PDCClientPlugin):
    def register(self):
        subcmd = self.add_command('global-component-list', help='list all global components')
        filters = ('dist_git_path contact_role email label name upstream_homepage upstream_scm_type '
                   'upstream_scm_url'.split())
        for arg in filters:
            subcmd.add_argument('--' + arg, dest='filter_' + arg)
        subcmd.set_defaults(func=self.list_global_components)

        subcmd = self.add_command('global-component-info', help='display details of a global component')
        subcmd.add_argument('global_component_id', metavar='GLOBAL_COMPONENT_ID')
        subcmd.set_defaults(func=self.global_component_info)

        subcmd = self.add_admin_command('global-component-update',
                                        help='update an existing global component')
        subcmd.add_argument('global_component_id', metavar='GLOBAL_COMPONENT_ID')
        self.add_global_component_arguments(subcmd)
        subcmd.set_defaults(func=self.global_component_update)

        subcmd = self.add_admin_command('global-component-create',
                                        help='create new global component')
        self.add_global_component_arguments(subcmd)
        subcmd.set_defaults(func=self.global_component_create)

    def add_global_component_arguments(self, parser):
        add_parser_arguments(parser, {
            'name': {},
            'dist_git_path': {}}
        )
        add_parser_arguments(parser, {
            'upstream__homepage': {'arg': 'homepage'},
            'upstream__scm_type': {'arg': 'scm-type'},
            'upstream__scm_url': {'arg': 'scm-url'}},
            group='Upstream (optional)')

    def list_global_components(self, args):
        filters = extract_arguments(args, prefix='filter_')
        if not filters:
            sys.stderr.write('At least some filter must be used.\n')
            sys.exit(1)
        global_components = get_paged(self.client['global-components']._, **filters)

        if args.json:
            print json.dumps(list(global_components))
            return

        if global_components:
            print '{:<10} {:45}'.format('ID', 'Global Component Name')
            for global_component in global_components:
                print '{:<10} {:45}'.format(
                      global_component['id'],
                      global_component['name'])

    def global_component_info(self, args, global_component_id=None):
        global_component_id = global_component_id or args.global_component_id
        global_component = self.client['global-components'][global_component_id]._()

        if args.json:
            print json.dumps(global_component)
            return

        fmt = '{:20} {}'
        print fmt.format('ID', global_component['id'])
        print fmt.format('Name', global_component['name'])
        print fmt.format('Dist Git Path', global_component['dist_git_path'] or '')
        print fmt.format('Dist Git URL', global_component['dist_git_web_url'] or '')
        if global_component['labels']:
            print 'Labels:'
            for label in global_component['labels']:
                print ''.join(['\t', label['name']])

        if global_component['upstream']:
            print 'Upstream:'
            for (k, v) in global_component['upstream'].iteritems():
                print ''.join(['\t', k, ':', '\t', v])

        if global_component['contacts']:
            print 'Contacts:'
            for global_component_contact in global_component['contacts']:
                print ''.join(['\tRole:\t', global_component_contact['contact_role']])
                for name in ('username', 'mail_name'):
                    if name in global_component_contact['contact']:
                        print ''.join(['\t\tName:\t', global_component_contact['contact'][name]])
                print ''.join(['\t\tEmail:\t', global_component_contact['contact']['email']])

    def global_component_create(self, args):
        data = extract_arguments(args)
        self.logger.debug('Creating global component with data %r', data)
        response = self.client['global-components']._(data)
        self.global_component_info(args, response['id'])

    def global_component_update(self, args):
        data = extract_arguments(args)
        if data:
            self.logger.debug('Updating global component %s with data %r',
                              args.global_component_id, data)
            self.client['global-components'][args.global_component_id]._ += data
        else:
            self.logger.debug('Empty data, skipping request')
        self.global_component_info(args)


class ReleaseComponentPlugin(PDCClientPlugin):
    def register(self):
        subcmd = self.add_command('release-component-list', help='list all release components')
        subcmd.add_argument('--include_inactive_release', action='store_true',
                            help='show both active and inactive release components')
        filters = ('active brew_package bugzilla_component contact_role email global_component name release srpm_name '
                   'type'.split())
        for arg in filters:
            subcmd.add_argument('--' + arg, dest='filter_' + arg)
        subcmd.set_defaults(func=self.list_release_components)

        subcmd = self.add_command('release-component-info', help='display details of a release component')
        subcmd.add_argument('release_component_id', metavar='RELEASE_COMPONENT_ID')
        subcmd.set_defaults(func=self.release_component_info)

        subcmd = self.add_admin_command('release-component-update',
                                        help='update an existing release component')
        subcmd.add_argument('release_component_id', metavar='RELEASE_COMPONENT_ID')
        self.add_release_component_arguments(subcmd)
        subcmd.set_defaults(func=self.release_component_update)

        subcmd = self.add_admin_command('release-component-create',
                                        help='create new release')
        self.add_release_component_arguments(subcmd)
        subcmd.add_argument('--release', dest='release')
        subcmd.add_argument('--global-component', dest='global_component')
        subcmd.set_defaults(func=self.release_component_create)

    def add_release_component_arguments(self, parser):
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--activate', action='store_const', const=True, dest='active')
        group.add_argument('--deactivate', action='store_const', const=False, dest='active')
        add_parser_arguments(parser, {
            'name': {},
            'dist_git_branch': {},
            'bugzilla_component': {},
            'brew_package': {},
            'type': {},
            'srpm__name': {'arg': 'srpm-name'}}
        )

    def list_release_components(self, args):
        filters = extract_arguments(args, prefix='filter_')
        if not filters:
            sys.stderr.write('At least some filter must be used.\n')
            sys.exit(1)
        release_components = get_paged(self.client['release-components']._, **filters)

        if args.json:
            print json.dumps(list(release_components))
            return

        if release_components:
            print '{:<10} {:15} {:45}'.format('ID', 'Release ID', 'Release Component Name')
            for release_component in release_components:
                print '{:<10} {:15} {:45}'.format(
                      release_component['id'],
                      release_component['release']['release_id'],
                      release_component['name'])

    def release_component_info(self, args, release_component_id=None):
        release_component_id = release_component_id or args.release_component_id
        release_component = self.client['release-components'][release_component_id]._()

        if args.json:
            print json.dumps(release_component)
            return

        fmt = '{:20} {}'
        print fmt.format('ID', release_component['id'])
        print fmt.format('Name', release_component['name'])
        print fmt.format('Release ID', release_component['release']['release_id'])
        print fmt.format('Global Component', release_component['global_component'])
        print fmt.format('Bugzilla Component', release_component['bugzilla_component'])
        print fmt.format('Brew Package', release_component['brew_package'])
        print fmt.format('Dist Git Branch', release_component['dist_git_branch'] or '')
        print fmt.format('Dist Git URL', release_component['dist_git_web_url'] or '')
        print fmt.format('Activity', 'active' if release_component['active'] else 'inactive')
        print fmt.format('Type', release_component['type'])
        print fmt.format('Srpm Name', release_component['srpm']['name'] if release_component['srpm'] else 'null')

        if release_component['contacts']:
            print 'Contacts:'
            for release_component_contact in release_component['contacts']:
                print ''.join(['\tRole:\t', release_component_contact['contact_role']])
                for name in ('username', 'mail_name'):
                    if name in release_component_contact['contact']:
                        print ''.join(['\t\tName:\t', release_component_contact['contact'][name]])
                print ''.join(['\t\tEmail:\t', release_component_contact['contact']['email']])

    def release_component_create(self, args):
        data = extract_arguments(args)
        if args.release is not None:
            data['release'] = args.release
        if args.global_component is not None:
            data['global_component'] = args.global_component
        if args.active is not None:
            data['active'] = args.active
        self.logger.debug('Creating release component with data %r', data)
        response = self.client['release-components']._(data)
        self.release_component_info(args, response['id'])

    def release_component_update(self, args):
        data = extract_arguments(args)
        if args.active is not None:
            data['active'] = args.active
        if data:
            self.logger.debug('Updating release component %s with data %r',
                              args.release_component_id, data)
            self.client['release-components'][args.release_component_id]._ += data
        else:
            self.logger.debug('Empty data, skipping request')
        self.release_component_info(args)


PLUGIN_CLASSES = [GlobalComponentPlugin, ReleaseComponentPlugin]
