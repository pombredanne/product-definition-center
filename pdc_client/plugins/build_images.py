# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Red Hat
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#
import json
import ast
import re

from pdc_client.plugin_helpers import PDCClientPlugin, get_paged, add_parser_arguments, extract_arguments


class BuildImagePlugin(PDCClientPlugin):
    def register(self):
        subcmd = self.add_command('build-image-list', help='list all build images')
        subcmd.add_argument('--show-md5', action='store_true',
                            help='whether to display md5 checksums')
        add_parser_arguments(subcmd, {'component_name': {},
                                      'rpm_version': {},
                                      'rpm_release': {},
                                      'image_id': {},
                                      'image_format': {},
                                      'md5': {},
                                      'archive_build_nvr': {},
                                      'archive_name': {},
                                      'archive_size': {},
                                      'archive_md5': {},
                                      'release_id': {}},
                             group='Filtering')

        subcmd.set_defaults(func=self.list_build_image)

        subcmd = self.add_command('build-image-info', help='display details of a build image')
        subcmd.add_argument('image_id', metavar='IMAGE_ID')
        subcmd.set_defaults(func=self.build_image_info)

        subcmd = self.add_admin_command('build-image-update',
                                        help='update an existing build image')
        subcmd.add_argument('image_id', metavar='IMAGE_ID')
        self.add_build_image_arguments(subcmd, True)
        subcmd.set_defaults(func=self.build_image_update)

        subcmd = self.add_admin_command('build-image-create',
                                        help='create new build image')
        self.add_build_image_arguments(subcmd)
        subcmd.set_defaults(func=self.build_image_create)

    def add_build_image_arguments(self, parser, is_update=False):
        argument_dic = {
            'image_format': {},
            'md5': {},
            'releases': {'nargs': '*', 'metavar': 'RELEASE_ID'},
            'rpms': {'nargs': '*', 'metavar': 'RPM_DATA_DICT', 'type': self._parse_to_dict},
            'archives': {'nargs': '*', 'metavar': 'ARCHIVE_DATA_DICT', 'type': self._parse_to_dict}

        }
        if not is_update:
            # 'create' must provide a unique image_id
            argument_dic['image_id'] = {}
        add_parser_arguments(parser, argument_dic)

    def _print_build_image_list(self, build_images, with_md5=False):
        fmt = '{image_id}'
        if with_md5:
            fmt += ' {md5}'
        for build_image in build_images:
            print fmt.format(**build_image)

    def list_build_image(self, args):
        filters = extract_arguments(args)
        build_images = get_paged(self.client['build-images']._, **filters)
        if args.json:
            print json.dumps(list(build_images))
            return
        self._print_build_image_list(build_images, args.show_md5)

    def build_image_info(self, args, image_id=None):
        image_id = image_id or args.image_id
        build_images = self.client['build-images']._(image_id=image_id)
        build_image = build_images['results'][0]

        if args.json:
            print json.dumps(build_image)
            return
        fmt = '{:20} {}'
        print fmt.format('Image ID', build_image['image_id'])
        print fmt.format('Image Format', build_image['image_format'])
        print fmt.format('URL', build_image['url'])
        print fmt.format('MD5', build_image['md5'])

        for key in ('releases', 'rpms'):
            if build_image[key]:
                print '\nRelated %s:' % key
                for value in build_image[key]:
                    print ' * {}'.format(value)

        if build_image['archives']:
            print '\nRelated archives:'
            fmt = '* {:40}{:60}{}'
            print fmt.format('MD5', 'Name', 'Build NVR')
            fmt = '  {:40}{:60}{}'
            for archive in build_image['archives']:
                print fmt.format(archive['md5'], archive['name'], archive['build_nvr'])

    def build_image_update(self, args):
        data = extract_arguments(args)
        if data and args.image_id:
            self.logger.debug('Updating build image {} with data {}'.format(args.image_id, data))
            pk = self._get_pk_from_image_id(args.image_id)
            response = self.client['build-images/%s' % pk]._("PATCH", data)
            self.build_image_info(args, response['image_id'])
        else:
            self.logger.info('No change required, not making a request')

    def build_image_create(self, args):
        data = extract_arguments(args)
        response = self.client['build-images']._(data)
        self.build_image_info(args, response['image_id'])

    def _get_pk_from_image_id(self, image_id):
        build_images = self.client['build-images']._(image_id=image_id)
        url = build_images['results'][0]['url']
        m = re.search('(\d+)/$', url)
        return m.group(1)

    def _parse_to_dict(self, in_str):
        result = ast.literal_eval(in_str)
        if isinstance(result, dict):
            return result
        raise ValueError("malformed string: %s" % in_str)


PLUGIN_CLASSES = [BuildImagePlugin]
