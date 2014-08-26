#!/usr/bin/env python2 -u

import glutabbix
from glutabbix import Glutabbix
import os
import pprint

if __name__ == '__main__':

    zabbix_url = 'http://zabbixserverbox/zabbix/api_jsonrpc.php'
    user = 'admin'
    password = 'zabbix'
    print("Login to Zabbix")
    zabbix = Glutabbix(zabbix_url, user, password)

    print("Get Template")
    output = zabbix.get_template('Template App MySQL')
    pp = pprint.PrettyPrinter(width=20)
    pp.pprint(output)

    print("export configuration")
    config = zabbix.export_configuration('templates', '100100000010100')

    print("read configuration from disk")
    with open('/tmp/lixo.xml') as f:
        config = f.read().replace('\n','')

    print("inport configuration into zabbix")
    output = zabbix.import_configuration(config)
    print(output)

    print("create hostgroup")
    output = zabbix.create_hostgroup('lixo2')
    print(output)

    print("get hostgroup details")
    groupid = (zabbix.get_hostgroup('lixo2'))[0]['groupid']
    print(groupid)

    print("delete hostgroup")
    output = zabbix.delete_hostgroup(groupid)
    print(output)

    interfaces = [
        {
            "type": 1,
            "main": 1,
            "useip": 1,
            "ip": "192.168.3.1",
            "dns": "",
            "port": "10050"
        }
    ]

    inventory = {}

    print("get template")
    templateid = zabbix.get_template('Template OS Linux')[0]['templateid']
    print(templateid)

    print("create host")
    output = zabbix.create_host('myhost',
                                interfaces,
                                groupid,
                                templateid,
                                inventory)


    print("get host details")
    output = zabbix.get_host('myhost')
    pp = pprint.PrettyPrinter()
    pp.pprint(output)
