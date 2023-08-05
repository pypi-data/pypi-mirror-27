# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Red Hat
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#
from pdc_client.test_helpers import CLITestCase
from pdc_client.runner import Runner


class GlobalComponentContactTestCase(CLITestCase):
    def setUp(self):
        self.runner = Runner()
        self.runner.setup()
        self.detail = {
            'id': '1',
            'component': 'Test Global Component',
            'role': 'pm',
            'contact': {
                'username': 'Test Contact',
                'email': 'test_contact@example.com',
            }
        }

    def _setup_detail(self, api):
        api.add_endpoint('global-component-contacts/1', 'GET', self.detail)

    def test_list_without_filters(self, api):
        with self.expect_failure():
            self.runner.run(['global-component-contact', 'list'])

    def test_list_multi_page(self, api):
        api.add_endpoint('global-component-contacts', 'GET', [
            {'id': x,
             'component': 'Test Global Component %s' % x,
             'role': 'watcher',
             'contact': {
                 'username': 'Test Contact',
                 'email': 'test_contact@example.com',
             }}
            for x in range(1, 26)
        ])
        with self.expect_output('global_component_contact/list_multi_page.txt'):
            self.runner.run(['global-component-contact', 'list',
                             '--role', 'watcher'])
        self.assertEqual(api.calls['global-component-contacts'],
                         [('GET', {'page': 1, 'role': 'watcher'}),
                          ('GET', {'page': 2, 'role': 'watcher'})])

    def test_detail(self, api):
        self._setup_detail(api)
        with self.expect_output('global_component_contact/detail.txt'):
            self.runner.run(['global-component-contact', 'info', '1'])
        self.assertEqual(api.calls,
                         {'global-component-contacts/1': [('GET', {})]})

    def test_delete(self, api):
        api.add_endpoint('global-component-contacts/1', 'DELETE', None)
        with self.expect_output('global_component_contact/empty.txt'):
            self.runner.run(['global-component-contact', 'delete', '1'])
        self.assertEqual(api.calls,
                         {'global-component-contacts/1': [('DELETE', {})]})

    def test_delete_matched(self, api):
        api.add_endpoint('global-component-contacts', 'GET', [self.detail])
        api.add_endpoint('global-component-contacts/1', 'DELETE', None)
        with self.expect_output('global_component_contact/empty.txt'):
            self.runner.run(['global-component-contact', 'delete-match', '--role', 'pm'])
        self.assertEqual(api.calls,
                         {'global-component-contacts': [('GET', {'page': 1,
                                                                 'role': 'pm'})],
                          'global-component-contacts/1': [('DELETE', {})]})

    def test_delete_multi_matches(self, api):
        api.add_endpoint('global-component-contacts', 'GET', [self.detail] * 2)
        with self.expect_output('global_component_contact/multi_matches.txt'):
            self.runner.run(['global-component-contact', 'delete-match', '--role', 'pm'])
        self.assertEqual(api.calls,
                         {'global-component-contacts': [('GET', {'page': 1,
                                                                 'role': 'pm'})]})

    def test_create(self, api):
        api.add_endpoint('global-component-contacts', 'POST', self.detail)
        self._setup_detail(api)
        with self.expect_output('global_component_contact/detail.txt'):
            self.runner.run(['global-component-contact', 'create',
                             '--component', 'Test Global Component',
                             '--role', 'pm',
                             '--username', 'Test Contact',
                             '--email', 'test_contact@example.com'])
        self.assertEqual(api.calls,
                         {'global-component-contacts':
                             [('POST',
                               {'component': 'Test Global Component',
                                'role': 'pm',
                                'contact': {
                                    'username': 'Test Contact',
                                    'email': 'test_contact@example.com'
                                }})],
                          'global-component-contacts/1': [('GET', {})]})

    def test_info_json(self, api):
        self._setup_detail(api)
        with self.expect_output('global_component_contact/detail.json', parse_json=True):
            self.runner.run(['--json', 'global-component-contact', 'info', '1'])
        self.assertEqual(api.calls,
                         {'global-component-contacts/1': [('GET', {})]})

    def test_list_json(self, api):
        api.add_endpoint('global-component-contacts', 'GET', [self.detail])
        with self.expect_output('global_component_contact/list.json', parse_json=True):
            self.runner.run(['--json', 'global-component-contact', 'list',
                             '--role', 'pm'])


class ReleaseComponentContactTestCase(CLITestCase):
    def setUp(self):
        self.runner = Runner()
        self.runner.setup()
        self.detail = {
            'id': '1',
            'component': {
                'name': 'Test Release Component',
                'release': 'test-release'
            },
            'role': 'pm',
            'contact': {
                'username': 'Test Contact',
                'email': 'test_contact@example.com',
            }
        }

    def _setup_detail(self, api):
        api.add_endpoint('release-component-contacts/1', 'GET', self.detail)

    def test_list_without_filters(self, api):
        with self.expect_failure():
            self.runner.run(['release-component-contact', 'list'])

    def test_list_multi_page(self, api):
        api.add_endpoint('release-component-contacts', 'GET', [
            {'id': x,
             'component': {
                 'name': 'Test Release Component %s' % x,
                 'release': 'test-release'
             },
             'role': 'watcher',
             'contact': {
                 'username': 'Test Contact',
                 'email': 'test_contact@example.com',
             }}
            for x in range(1, 26)
        ])
        with self.expect_output('release_component_contact/list_multi_page.txt'):
            self.runner.run(['release-component-contact', 'list', '--role', 'watcher'])
        self.assertEqual(api.calls['release-component-contacts'],
                         [('GET', {'page': 1, 'role': 'watcher'}),
                          ('GET', {'page': 2, 'role': 'watcher'})])

    def test_detail(self, api):
        self._setup_detail(api)
        with self.expect_output('release_component_contact/detail.txt'):
            self.runner.run(['release-component-contact', 'info', '1'])
        self.assertEqual(api.calls,
                         {'release-component-contacts/1': [('GET', {})]})

    def test_delete(self, api):
        api.add_endpoint('release-component-contacts/1', 'DELETE', None)
        with self.expect_output('release_component_contact/empty.txt'):
            self.runner.run(['release-component-contact', 'delete', '1'])
        self.assertEqual(api.calls,
                         {'release-component-contacts/1': [('DELETE', {})]})

    def test_delete_matched(self, api):
        api.add_endpoint('release-component-contacts', 'GET', [self.detail])
        api.add_endpoint('release-component-contacts/1', 'DELETE', None)
        with self.expect_output('release_component_contact/empty.txt'):
            self.runner.run(['release-component-contact', 'delete-match', '--role', 'pm'])
        self.assertEqual(api.calls,
                         {'release-component-contacts': [('GET', {'page': 1,
                                                                  'role': 'pm'})],
                          'release-component-contacts/1': [('DELETE', {})]})

    def test_delete_multi_matches(self, api):
        api.add_endpoint('release-component-contacts', 'GET', [self.detail] * 2)
        with self.expect_output('release_component_contact/multi_matches.txt'):
            self.runner.run(['release-component-contact', 'delete-match', '--role', 'pm'])
        self.assertEqual(api.calls,
                         {'release-component-contacts': [('GET', {'page': 1,
                                                                  'role': 'pm'})]})

    def test_create(self, api):
        api.add_endpoint('release-component-contacts', 'POST', self.detail)
        self._setup_detail(api)
        with self.expect_output('release_component_contact/detail.txt'):
            self.runner.run(['release-component-contact', 'create',
                             '--release', 'test-release',
                             '--component', 'Test Release Component',
                             '--role', 'pm',
                             '--username', 'Test Contact',
                             '--email', 'test_contact@example.com'])
        self.assertEqual(api.calls,
                         {'release-component-contacts':
                             [('POST',
                               {
                                   'component': {
                                       'name': 'Test Release Component',
                                       'release': 'test-release'
                                   },
                                   'role': 'pm',
                                   'contact': {
                                       'username': 'Test Contact',
                                       'email': 'test_contact@example.com'
                                   }
                               })],
                          'release-component-contacts/1': [('GET', {})]})

    def test_info_json(self, api):
        self._setup_detail(api)
        with self.expect_output('release_component_contact/detail.json', parse_json=True):
            self.runner.run(['--json', 'release-component-contact', 'info', '1'])
        self.assertEqual(api.calls,
                         {'release-component-contacts/1': [('GET', {})]})

    def test_list_json(self, api):
        api.add_endpoint('release-component-contacts', 'GET', [self.detail])
        with self.expect_output('release_component_contact/list.json', parse_json=True):
            self.runner.run(['--json', 'release-component-contact', 'list',
                             '--role', 'pm'])
