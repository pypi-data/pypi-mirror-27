# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Red Hat
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

from __future__ import print_function

from pdc_client.plugin_helpers import (PDCClientPlugin,
                                       extract_arguments,
                                       add_create_update_args)

_FIELD_WITH_NAME = [
    ("id", "ID"),
    ("release_id", "Release ID"),
    ("variant_uid", "Variant UID"),
    ("arch", "Arch"),
    ("service", "Service"),
    ("name", "Name"),
    ("repo_family", "Repo Family"),
    ("content_format", "Content Format"),
    ("content_category", "Content Category"),
    ("shadow", "Shadow"),
    ("product_id", "Product ID"),
]

_ORDERING = [
    'variant_arch__variant__release__release_id',
    'variant_arch__variant__variant_uid',
    'variant_arch__arch__name',
    'service',
    'repo_family',
    'content_format',
    'content_category',
    'shadow',
    'name'
]


class RepoPlugin(PDCClientPlugin):
    command = 'content-delivery-repo'

    def register(self):
        self.set_command()

        list_parser = self.add_action('list', help='list all content delivery repos')
        filters = ('arch', 'content-category', 'content-format', 'name', 'release-id',
                   'repo-family', 'service', 'shadow', 'variant-uid', 'product-id')
        for arg in filters:
            list_parser.add_argument('--' + arg, dest='filter_' + arg.replace('-', '_'))
        list_parser.set_defaults(func=self.repo_list)

        info_parser = self.add_action('info', help='display details of an content delivery repo')
        info_parser.add_argument('repoid', metavar='ID')
        info_parser.set_defaults(func=self.repo_info)

        create_parser = self.add_action('create', help='create a new content delivery repo')
        self.add_repo_arguments(create_parser, required=True)
        create_parser.set_defaults(func=self.repo_create)

        clone_parser = self.add_action('clone', help='clone repos from one release to another',
                                       description='The include-* options are used to filter '
                                                   'which releases should be cloned. If any are '
                                                   'omitted, all values for that attribute will '
                                                   'be cloned.')
        self.add_clone_arguments(clone_parser)
        clone_parser.set_defaults(func=self.repo_clone)

        update_parser = self.add_action('update', help='update an existing content delivery repo')
        update_parser.add_argument('repoid', metavar='ID')
        self.add_repo_arguments(update_parser)
        update_parser.set_defaults(func=self.repo_update)

        delete_parser = self.add_action('delete', help='delete an existing content delivery repo')
        delete_parser.add_argument('repoid', metavar='ID', type=int, nargs='+')
        delete_parser.set_defaults(func=self.repo_delete)

        # export
        # This command is almost identical to the 'list' command.
        # It is intentional to keep it as a separate command,
        # because it's tailored to a certain use case:
        #  * export repos from a release
        #  * dump the repos to a JSON file
        #  * edit data (change release_id, change versions in repo names)
        #  * import repos to a new release
        export_parser = self.add_action('export', help='export repos from a release into a json file')
        export_parser.add_argument('release_id')
        export_parser.add_argument('json_file')
        self.add_repo_arguments(export_parser, exclude=['release_id'])
        export_parser.set_defaults(func=self.repo_export)

        # import
        import_parser = self.add_action('import', help='import repos from a json file into a release')
        import_parser.add_argument('release_id')
        import_parser.add_argument('json_file')
        import_parser.set_defaults(func=self.repo_import)

    def add_repo_arguments(self, parser, required=False, exclude=None):
        required_args = {
            'arch': {},
            'content_category': {},
            'content_format': {},
            'name': {},
            'release_id': {},
            'repo_family': {},
            'service': {},
            'variant_uid': {}
        }
        optional_args = {'product_id': {'type': int},
                         'shadow': {'help': 'default is false when create a content delivery repo',
                                    'metavar': 'SHADOW_FLAG'}}

        if exclude:
            # TODO: consider moving this into add_create_update_args()
            for i in exclude:
                required_args.pop(i, None)
                optional_args.pop(i, None)

        add_create_update_args(parser, required_args, optional_args, required)

    def add_clone_arguments(self, parser):
        necessary_args = {
            'release_id_from': {'metavar': 'RELEASE_ID_FROM'},
            'release_id_to': {'metavar': 'RELEASE_ID_TO'},
        }
        optional_args = {
            'include_service': {'nargs': '*', 'metavar': 'SERVICE'},
            'include_repo_family': {'nargs': '*', 'metavar': 'REPO_FAMILY'},
            'include_content_format': {'nargs': '*', 'metavar': 'CONTENT_FORMAT'},
            'include_content_category': {'nargs': '*', 'metavar': 'CONTENT_CATEGORY'},
        }
        add_create_update_args(parser, necessary_args, optional_args, True)

        shadow_group = parser.add_mutually_exclusive_group()
        shadow_group.add_argument('--include-shadow', action='store_true')
        shadow_group.add_argument('--exclude-shadow', action='store_false', dest='include_shadow')

        optional_args = {
            'include_product_id': {'metavar': 'PRODUCT_ID', 'type': int},
        }
        add_create_update_args(parser, {}, optional_args, False)

        self.run_hook('repo_parser_setup', parser)

    def repo_list(self, args, data=None):
        filters = extract_arguments(args, prefix='filter_')
        if not filters and not data:
            self.subparsers.choices.get('list').error('At least some filter must be used.')
        ordering = ','.join(_ORDERING)
        repos = data or self.client.get_paged(self.client['content-delivery-repos']._, ordering=ordering, **filters)

        if args.json:
            print(self.to_json(list(repos)))
            return

        # Create transposed table before printing to find out minimal
        # widths for each column.
        columns = [[name] for _, name in _FIELD_WITH_NAME]
        for repo in repos:
            for index, column in enumerate(columns):
                field = _FIELD_WITH_NAME[index][0]
                value = repo[field]
                if value is None:
                    value = ""
                column.append(value)

        # Create formating string for rows.
        fmt = ''
        for index, column in enumerate(columns):
            width = max([len(str(cell)) for cell in column])
            fmt += '{' + str(index) + ':' + str(width) + '}  '
        fmt = fmt.rstrip()

        # Transpose table and print.
        rows = zip(*columns)
        for row in rows:
            print(fmt.format(*row))

    def repo_info(self, args, repo_id=None):
        response = self.client['content-delivery-repos'][repo_id or args.repoid]._()

        if args.json:
            print(self.to_json(response))
            return

        fmt = '{0:20} {1}'
        for field, name in _FIELD_WITH_NAME:
            value = response[field]
            if value is None:
                value = ""
            print(fmt.format(name, value))

    def repo_create(self, args):
        data = extract_arguments(args)
        self.logger.debug('Creating content delivery repo with data %r', data)
        response = self.client['content-delivery-repos']._(data)
        self.repo_info(args, response['id'])

    def repo_clone(self, args):
        data = self.get_repo_data(args)
        self.logger.debug('Clone repos with data {0}'.format(data))
        response = self.client.rpc['content-delivery-repos'].clone._(data)
        self.repo_list(args, response)

    def repo_update(self, args):
        data = extract_arguments(args)
        if data:
            self.logger.debug('Updating ontent delivery repo %s with data %r', args.repoid, data)
            self.client['content-delivery-repos'][args.repoid]._ += data
        else:
            self.logger.debug('Empty data, skipping request')
        self.repo_info(args)

    def repo_delete(self, args):
        repo_id_list = args.repoid
        for repo_id in repo_id_list:
            self.logger.debug('Deleting content delivery repo: %s', repo_id)
        self.client['content-delivery-repos']._("DELETE", repo_id_list)

    def get_repo_data(self, args):
        data = extract_arguments(args)
        if args.include_shadow is not None:
            data['include_shadow'] = args.include_shadow

        self.run_hook('repo_parser_setup', args, data)

        return data

    def repo_export(self, args):
        filters = extract_arguments(args, prefix='data__')
        filters["release_id"] = args.release_id
        repos = self.client.get_paged(self.client['content-delivery-repos']._, **filters)
        repos = list(repos)
        for repo in repos:
            # remove IDs, they are not needed for import
            repo.pop("id")

        with open(args.json_file, "w") as f:
            f.write(self.to_json(repos))

    def repo_import(self, args):
        release_id = args.release_id

        with open(args.json_file, "r") as f:
            repos = self.from_json(f.read())

        for repo in repos:
            # remove IDs, new ones will be assigned to the new repos
            repo.pop("id", None)
            if repo["release_id"] != release_id:
                raise ValueError("Inconsistent release_id provided by user '{0}' vs. found in json '{1}'.".format(release_id, repo["release_id"]))

        self.client['content-delivery-repos']._(repos)


PLUGIN_CLASSES = [RepoPlugin]
