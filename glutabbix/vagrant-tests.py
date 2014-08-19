#!/usr/bin/env python2

import glutabbix
from glutabbix import Glutabbix
import os
import pprint

if __name__ == '__main__':

    zabbix_url = 'http://zabbixserverbox/zabbix/api_jsonrpc.php'
    user = 'admin'
    password = 'zabbix'
    zabbix = Glutabbix(zabbix_url, user, password)

    output = zabbix.get_template('Template App MySQL')
    pp = pprint.PrettyPrinter(width=20)
    pp.pprint(output)

    config = zabbix.export_configuration('templates', '100100000010100')

    with open('/tmp/lixo.xml') as f:
        config = f.read().replace('\n','')

    output = zabbix.import_configuration(config)
    print(output)

    output = zabbix.create_hostgroup('lixo2')
    print(output)

    groupid = (zabbix.get_hostgroup('lixo2'))[0]['groupid']
    print(groupid)

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

    templateid = zabbix.get_template('lixo2')[0]['templateid']
    print(templateid)

    output = zabbix.create_host('myhost',
                                interfaces,
                                groupid,
                                templateid,
                                inventory)


    output = zabbix.get_host('craphost')
    os.system('cls')
    pp = pprint.PrettyPrinter()
    pp.pprint(output)
