#!/usr/bin/env python2

import requests
import json
# from requests import ConnectionError
# import pprint


class Glutabbix:

    def __init__(self, zabbix_url, user, password):
        """ Creates a new instance of the Class Glutabbix and returns a login handle.
            For example:

            >>> zabbix_url = 'http://zabbixserverbox/zabbix/api_jsonrpc.php'
            >>> zabbix = Glutabbix(zabbix_url, 'admin', 'password')
            >>> zabbix.auth #doctest: +ELLIPSIS
            u'...'

        """
        self.zabbix_url = zabbix_url
        self.user = user
        self.password = password

        obj = self._build_request_call_for_login('admin', 'password')
        self.auth = self.api_request(obj)

    """
    _build_request_call functions_for_<zabbix api method>

    return a dictionary for the zabbix api call in question.
    this dictionary can then be consumed by the api_request method
    which sends a json api request to zabbix.
    """

    def _build_request_call_for_login(self, user, password):
        """ returns a JSON API string for the login call
            For example:

            >>> zabbix_url = 'http://zabbixserverbox/zabbix/api_jsonrpc.php'
            >>> user = 'admin'
            >>> password = 'password'
            >>> zabbix = Glutabbix(zabbix_url, user, password)
            >>> obj = zabbix._build_request_call_for_login(user, password)
            >>> import pprint
            >>> pp = pprint.PrettyPrinter(width=60)
            >>> pp.pprint(obj) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
             {'id': 1,
             'jsonrpc': '2.0',
             'method': 'user.login',
              'params': {'password': 'password', 'user': 'admin'}}
        """
        return {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": user,
                "password": password
            },
            "id": 1
        }

    def _build_request_call_for_template_get(self, template_name):
        """ returns a JSON API string for the get.template call
            For example:

            >>> zabbix_url = 'http://zabbixserverbox/zabbix/api_jsonrpc.php'
            >>> user = 'admin'
            >>> password = 'password'
            >>> template = 'My Fat Template'
            >>> zabbix = Glutabbix(zabbix_url, user, password)
            >>> obj = zabbix._build_request_call_for_template_get(template)
            >>> import pprint
            >>> pp = pprint.PrettyPrinter(width=60)
            >>> pp.pprint(obj) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
            {'auth': u'...',
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'template.get',
            'params': {'filter': {'host': ['My Fat Template']},
                      'output': 'extend'}}
        """

        return {
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "extend",
                "filter": {
                    "host": [template_name]
                }
            },
            "auth": self.auth,
            "id": 1
        }

    def _build_request_call_for_template_delete(self, templateid):
        """ returns a JSON API string for the get.template call
            For example:

            >>> zabbix_url = 'http://zabbixserverbox/zabbix/api_jsonrpc.php'
            >>> user = 'admin'
            >>> password = 'password'
            >>> template = 'My Fat Template'
            >>> zabbix = Glutabbix(zabbix_url, user, password)
            >>> obj = zabbix._build_request_call_for_template_delete(template)
            >>> import pprint
            >>> pp = pprint.PrettyPrinter(width=60)
            >>> pp.pprint(obj) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
            {'auth': u'...',
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'template.delete',
            'params': ['My Fat Template']}
        """

        return {
            "jsonrpc": "2.0",
            "method": "template.delete",
            "params": [
                templateid,
            ],
            "auth": self.auth,
            "id": 1
        }

    def _build_request_call_for_item_get(self, object_type, object_id):
        return {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "extend",
                object_type: object_id,
                "sortfield": "name"
            },
            "auth": self.auth,
            "id": 1
        }

    def _build_request_call_for_item_create(self, item):
        return {
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": item,
            "auth": self.auth,
            "id": 1
        }

    def _build_request_call_for_item_update(self, item):
        return {
            "jsonrpc": "2.0",
            "method": "item.update",
            "params": item,
            "auth": self.auth,
            "id": 1
        }

    def _build_request_call_for_configuration_export(self,
                                                     object_type, object_id):
        """ returns a JSON API string for the configuration.export call
            For example:

            >>> zabbix_url = 'http://zabbixserverbox/zabbix/api_jsonrpc.php'
            >>> user = 'admin'
            >>> password = 'password'
            >>> template = 'My Fat Template'
            >>> zabbix = Glutabbix(zabbix_url, user, password)
            >>> obj = zabbix._build_request_call_for_configuration_export(
            ...    'template', '100100000010100')
            >>> import pprint
            >>> pp = pprint.PrettyPrinter(width=60)
            >>> pp.pprint(obj) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
            {'auth': u'...',
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'configuration.export',
            'params': {'format': 'json',
                        'options': {'template': ['100100000010100']}}}
        """
        return {
            "jsonrpc": "2.0",
            "method": "configuration.export",
            "params": {
                "options": {
                    object_type: [
                       object_id
                    ]
                },
                "format": "json"
            },
            "auth": self.auth,
            "id": 1
        }

    def _build_request_call_for_configuration_import(self, configuration):
        """ returns a JSON API string for the configuration.import call
            For example:

            >>> zabbix_url = 'http://zabbixserverbox/zabbix/api_jsonrpc.php'
            >>> user = 'admin'
            >>> password = 'password'
            >>> template = 'My Fat Template'
            >>> zabbix = Glutabbix(zabbix_url, user, password)
            >>> config = {"zabbix_export":
            ... {"version":"2.0",
            ... "date":"2014-08-13T10:11:20Z",
            ... "groups":[{"name":"Templates"}],
            ... "templates":[{"template":"Template App POP Service",
            ... "name":"Template App POP Service",
            ... "groups":[{"name":"Templates"}],
            ... "applications":[{"name":"POP service"}],
            ... "items":[{"name":"POP service is running",
            ... "type":"3",
            ... "snmp_community":"",
            ... "multiplier":"0",
            ... "snmp_oid":"",
            ... "key":"net.tcp.service[pop]",
            ... "delay":"60",
            ... "history":"7",
            ... "trends":"365",
            ... "status":"0",
            ... "value_type":"3",
            ... "allowed_hosts":"",
            ... "units":"",
            ... "delta":"0",
            ... "snmpv3_contextname":"",
            ... "snmpv3_securityname":"",
            ... "snmpv3_securitylevel":"0",
            ... "snmpv3_authprotocol":"0",
            ... "snmpv3_authpassphrase":"",
            ... "snmpv3_privprotocol":"0",
            ... "snmpv3_privpassphrase":"",
            ... "formula":"1",
            ... "delay_flex":"",
            ... "params":"",
            ... "ipmi_sensor":"",
            ... "data_type":"0",
            ... "authtype":"0",
            ... "username":"",
            ... "password":"",
            ... "publickey":"",
            ... "privatekey":"",
            ... "port":"",
            ... "description":"",
            ... "inventory_link":"0",
            ... "applications":[{"name":"POP service"}],
            ... "valuemap":{"name":"Service state"}}],
            ... "discovery_rules":[],
            ... "macros":[],
            ... "templates":[],
            ... "screens":[]}],
            ... "triggers":[
            ...     {"expression":"{Template App POP Service:net.tcp.service[pop].max(#3)}=0",
            ...      "name":"POP service is down on {HOST.NAME}",
            ...      "url":"",
            ...      "status":"0",
            ...      "priority":"3",
            ...      "description":"",
            ...      "type":"0",
            ...      "dependencies":[]
            ...     }]}}

            >>> obj = zabbix._build_request_call_for_configuration_import(config)
            >>> import pprint
            >>> pp = pprint.PrettyPrinter(width=60)
            >>> pp.pprint(obj) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
            {'auth': u'...',
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'configuration.import',
            'params': {'format': 'json',
            'rules': {'graphs': {'createMissing': True,
            'updateExisting': True},
            'groups': {'createMissing': True},
            'hosts': {'createMissing': True,
            'updateExisting': True},
            'items': {'createMissing': True,
            'updateExisting': True},
            'screens': {'createMissing': True,
            'updateExisting': True},
            'templateScreens': {'createMissing': True,
            'updateExisting': True},
            'templates': {'createMissing': True,
            'updateExisting': True}},
            'source': {'zabbix_export': {'date': '...',
            'groups': [{'name': 'Templates'}],
            'templates': [{'applications': [{'name': 'POP service'}],
            'discovery_rules': [],
            'groups': [{'name': 'Templates'}],
            'items': [{'allowed_hosts': '',
            'applications': [{'name': 'POP service'}],
            'authtype': '0',
            'data_type': '0',
            'delay': '60',
            'delay_flex': '',
            'delta': '0',
            'description': '',
            'formula': '1',
            'history': '7',
            'inventory_link': '0',
            'ipmi_sensor': '',
            'key': 'net.tcp.service[pop]',
            'multiplier': '0',
            'name': 'POP service is running',
            'params': '',
            'password': '',
            'port': '',
            'privatekey': '',
            'publickey': '',
            'snmp_community': '',
            'snmp_oid': '',
            'snmpv3_authpassphrase': '',
            'snmpv3_authprotocol': '0',
            'snmpv3_contextname': '',
            'snmpv3_privpassphrase': '',
            'snmpv3_privprotocol': '0',
            'snmpv3_securitylevel': '0',
            'snmpv3_securityname': '',
            'status': '0',
            'trends': '365',
            'type': '3',
            'units': '',
            'username': '',
            'value_type': '3',
            'valuemap': {'name': 'Service state'}}],
            'macros': [],
            'name': 'Template App POP Service',
            'screens': [],
            'template': 'Template App POP Service',
            'templates': []}],
            'triggers': [{'dependencies': [],
            'description': '',
            'expression': '{Template App POP Service:net.tcp.service[pop].max(#3)}=0',
            'name': 'POP service is down on {HOST.NAME}',
            'priority': '3',
            'status': '0',
            'type': '0',
            'url': ''}],
            'version': '2.0'}}}}
        """
        return {
            "jsonrpc": "2.0",
            "method": "configuration.import",
            "params": {
                "rules": {
                    "templates": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "screens": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "templateScreens": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "graphs": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "hosts": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "items": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "groups": {
                        "createMissing": True
                    }
                },
                "format": "json",
                "source": configuration
            },
            "auth": self.auth,
            "id": 1
        }

    def _build_request_call_for_hostgroup_create(self, hostgroup):
        """ returns a JSON API string for the hostgroup.create call
            For example:

            >>> zabbix_url = 'http://zabbixserverbox/zabbix/api_jsonrpc.php'
            >>> user = 'admin'
            >>> password = 'password'
            >>> zabbix = Glutabbix(zabbix_url, user, password)
            >>> obj = zabbix._build_request_call_for_hostgroup_create(
            ... 'NewHostGrp')
            >>> import pprint
            >>> pp = pprint.PrettyPrinter(width=60)
            >>> pp.pprint(obj) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
            {'auth': u'...',
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'hostgroup.create',
            'params': {'name': 'NewHostGrp'}}
        """
        return {
            "jsonrpc": "2.0",
            "method": "hostgroup.create",
            "params": {
                "name": hostgroup
            },
            "auth": self.auth,
            "id": 1
        }

    def _build_request_call_for_hostgroup_delete(self, hostgroup_id=[]):
        """ returns a JSON API string for the hostgroup.delete call
            For example:

            >>> zabbix_url = 'http://zabbixserverbox/zabbix/api_jsonrpc.php'
            >>> user = 'admin'
            >>> password = 'password'
            >>> zabbix = Glutabbix(zabbix_url, user, password)
            >>> obj = zabbix._build_request_call_for_hostgroup_delete(
            ... 'NewHostGrp')
            >>> import pprint
            >>> pp = pprint.PrettyPrinter(width=60)
            >>> pp.pprint(obj) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
            {'auth': u'...',
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'hostgroup.delete',
            'params': ['NewHostGrp']}
        """
        return {
            "jsonrpc": "2.0",
            "method": "hostgroup.delete",
            "params": [
                hostgroup_id
            ],
            "auth": self.auth,
            "id": 1
        }

    def _build_request_call_for_hostgroup_get(self, hostgroup):
        """ returns a JSON API string for the hostgroup.get call
            For example:

            >>> zabbix_url = 'http://zabbixserverbox/zabbix/api_jsonrpc.php'
            >>> user = 'admin'
            >>> password = 'password'
            >>> zabbix = Glutabbix(zabbix_url, user, password)
            >>> obj = zabbix._build_request_call_for_hostgroup_get('NewHostGrp')
            >>> import pprint
            >>> pp = pprint.PrettyPrinter(width=60)
            >>> pp.pprint(obj) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
            {'auth': u'...',
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'hostgroup.get',
            'params': {'filter': {'name': ['NewHostGrp']}, 'output': 'extend'}}
        """
        return {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
                "filter": {
                    "name": [hostgroup]
                }
            },
            "auth": self.auth,
            "id": 1
        }

    def _build_request_call_for_host_create(self, host, interfaces,
                                            groupid, templateid, inventory):
        """ returns a JSON API string for the host.create call
            For example:

            >>> zabbix_url = 'http://zabbixserverbox/zabbix/api_jsonrpc.php'
            >>> user = 'admin'
            >>> password = 'password'
            >>> zabbix = Glutabbix(zabbix_url, user, password)

            >>> interfaces = [
            ...                 {
            ...                     "type": 1,
            ...                     "main": 1,
            ...                     "useip": 1,
            ...                     "ip": "192.168.3.1",
            ...                     "dns": "",
            ...                     "port": "10050"
            ...                 }
            ...             ]

            >>> inventory = {"macaddress_a": "01232"}

            >>> groupid = '100100000000131'
            >>> templateid = '100100000000131'

            >>> obj = zabbix._build_request_call_for_host_create(
            ...    'newhost',
            ...    interfaces,
            ...    groupid,
            ...    templateid,
            ...    inventory)

            >>> import pprint
            >>> pp = pprint.PrettyPrinter(width=60)
            >>> pp.pprint(obj) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
            {'auth': u'...',
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'host.create',
            'params': {'groups': [{'groupid': '...131'}],
            'host': 'newhost',
            'interfaces': [{'dns': '',
            'ip': '192.168.3.1',
            'main': 1,
            'port': '10050',
            'type': 1,
            'useip': 1}],
            'inventory': {'macaddress_a': '01232'},
            'templates': [{'templateid': '...131'}]}}
        """
        return {
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": host,
                "interfaces": interfaces,
                "groups": [
                    {
                        "groupid": groupid
                    }
                ],
                "templates": [
                    {
                        "templateid": templateid
                    }
                ],
                "inventory": inventory
            },
            "auth": self.auth,
            "id": 1
        }

    def _build_request_call_for_host_get(self,object_name):
        """ returns a JSON API string for the host.get call
            For example:

            >>> zabbix_url = 'http://zabbixserverbox/zabbix/api_jsonrpc.php'
            >>> user = 'admin'
            >>> password = 'password'
            >>> zabbix = Glutabbix(zabbix_url, user, password)

            >>> obj = zabbix._build_request_call_for_host_get('myhost')

            >>> import pprint
            >>> pp = pprint.PrettyPrinter(width=60)
            >>> pp.pprint(obj) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
            {'auth': u'...',
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'host.get',
            'params': {'filter': {'host': ['myhost']},
                                        'output': 'extend'}}

        """
        return {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "filter": {
                "host": [ object_name ]
                }
            },
            "auth": self.auth,
            "id": 1
        }

    def _build_request_call_for_host_delete(self,object_name):
        """ returns a JSON API string for the host.delete call
            For example:

            >>> zabbix_url = 'http://zabbixserverbox/zabbix/api_jsonrpc.php'
            >>> user = 'admin'
            >>> password = 'password'
            >>> zabbix = Glutabbix(zabbix_url, user, password)

            >>> obj = zabbix._build_request_call_for_host_delete('myhost')

            >>> import pprint
            >>> pp = pprint.PrettyPrinter(width=60)
            >>> pp.pprint(obj) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
            {'auth': u'...',
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'host.delete',
            'params': [{'hostid': '...'}]}
        """
        return {
            "jsonrpc": "2.0",
            "method": "host.delete",
            "params": [
                { "hostid": '...' }
            ],
            "auth": self.auth,
            "id": 1
        }
    def api_request(self, obj):
        """
            api_request consumes a dictionary obj from the
            _build_request_call_for_<api_method> functions
            and performs the api request against zabbix
        """
        headers = {'content-type': 'application/json'}
        request = requests.post(self.zabbix_url,
                                data=json.dumps(obj),
                                headers=headers)
        response_dict = json.loads(request.text)
        if 'error' in response_dict:
            print('An error occurred! %s' % response_dict["error"])
        else:
            return response_dict['result']

    def get_template(self, template_name):
        """
            get_template returns a dictionary for a zabbix template
        """
        obj = self._build_request_call_for_template_get(template_name)
        template = self.api_request(obj)
        return template

    def delete_template(self, templateid):
        """
            deletes a zabbix template
        """
        obj = self._build_request_call_for_template_delete(templateid)
        output = self.api_request(obj)
        return output

    def get_items(self, object_type, object_id):
        """
            retrieves the items from an object (templateid, hostid)
        """
        obj = self._build_request_call_for_item_get(object_type,
                                                    object_id)
        output = self.api_request(obj)
        return output

    def create_item(self, item):
        """
            creates an item
        """
        obj = self._build_request_call_for_item_create(item)
        output = self.api_request(obj)
        return output

    def update_item(self, item):
        """
            update an item
        """
        obj = self._build_request_call_for_item_update(item)
        output = self.api_request(obj)
        return output

    def export_configuration(self, object_type, object_id):
        """
            export configuration block for an object
        """
        obj = self._build_request_call_for_configuration_export(object_type,
                                                                object_id)
        output = self.api_request(obj)
        return output

    def import_configuration(self, configuration):
        """
            import configuration block for an object
        """
        obj = self._build_request_call_for_configuration_import(configuration)
        output = self.api_request(obj)
        return output

    def create_hostgroup(self, hostgroup):
        """
            creates an hostgroup
        """
        obj = self._build_request_call_for_hostgroup_create(hostgroup)
        output = self.api_request(obj)
        return output

    def delete_hostgroup(self, hostgroup_id):
        """
            delete an hostgroup
        """
        obj = self._build_request_call_for_hostgroup_delete(hostgroup_id)
        output = self.api_request(obj)
        return output

    def get_hostgroup(self, hostgroup):
        """ Returns a hostgroup dictionary,
            Example:

            >>> zabbix_url = 'http://zabbixserverbox/zabbix/api_jsonrpc.php'
            >>> user = 'admin'
            >>> password = 'password'
            >>> hostgroup = 'Templates'
            >>> zabbix = Glutabbix(zabbix_url, user, password)
            >>> obj = zabbix.get_hostgroup(hostgroup)
            >>> import pprint
            >>> pp = pprint.PrettyPrinter(width=60)
            >>> pp.pprint(obj) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
            [{u'flags': u'...',
            u'groupid': u'...',
            u'internal': u'...',
            u'name': u'Templates'}]
        """
        obj = self._build_request_call_for_hostgroup_get(hostgroup)
        output = self.api_request(obj)
        return output

    def create_host(self, host, interfaces, groupid, templateid, inventory):
        """
            creates a host
        """
        obj = self._build_request_call_for_host_create(host,
                                                       interfaces,
                                                       groupid,
                                                       templateid,
                                                       inventory)
        output = self.api_request(obj)
        return output


    def get_host(self, hostname):
        """
            returns json data about a host
        """
        obj = self._build_request_call_for_host_get(hostname)
        output = self.api_request(obj)
        return output

    def delete_host(self, hostname):
        """
            deletes host
        """
        obj = self._build_request_call_for_host_delete(hostname)
        output = self.api_request(obj)
        return output
