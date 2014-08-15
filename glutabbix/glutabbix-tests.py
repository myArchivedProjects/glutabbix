#!/usr/bin/env python2

import glutabbix
from glutabbix import Glutabbix
import doctest
import os
import pprint
#import requests
#from sure import expect
#import httpretty
#import json

#def test_one():
    #result = json.dumps({'id': 1,
        #'jsonrpc': '2.0',
        #'method': 'user.login',
        #'params': {'password': 'password', 'user': 'admin'}})

    ## enable HTTPretty so that it will monkey patch the socket module
    #httpretty.enable()
    #httpretty.register_uri(httpretty.GET,
                           #"http://zabbixserverbox/zabbix/api_jsonrpc.php",
                           #body=result,
                           #status=200,
                           #content_type='text/json')


    #response = requests.get('http://zabbixserverbox/zabbix/api_jsonrpc.php')

    #assert response.text == result

     ##disable afterwards, so that you will have no problems in code that uses that socket module
    #httpretty.disable()

     ##reset HTTPretty state (clean up registered urls and request history)
    #httpretty.reset()    # reset HTTPretty state (clean up registered urls and request history)



if __name__ == '__main__':
    nfail, ntests = doctest.testmod(glutabbix)
    quit()

    zabbix_url = 'http://zabbixserverbox/zabbix/api_jsonrpc.php'
    user = 'admin'
    password = 'zabbix'
    zabbix = Glutabbix(zabbix_url, user, password)
    output = zabbix.get_template('Limiter')
    print(output)

#    output = zabbix.create_template("test lixo", 100100000000001)
#    pprint.pprint(output)


    config = zabbix.export_configuration('templates', '100100000010100')
    print(config)
#    output = zabbix.delete_template('100100000010129')
#    print(output)
    output = zabbix.import_configuration(config)
    print(output)

    output = zabbix._build_request_call_for_hostgroup_create('lixo2')
    print(output)
    output = zabbix.create_hostgroup('lixo2')
    print(output)

    groupid = (zabbix.get_hostgroup('lixo2'))[0]['groupid']
    print(groupid)

    #output = zabbix.delete_hostgroup(groupid)
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

    #inventory = {"macaddress_a": "01232"}
    inventory = {}

    templateid = zabbix.get_template('lixo2')[0]['templateid']
    print(templateid)

    output = zabbix._build_request_call_for_host_create('myhost',
                                                        interfaces,
                                                        groupid,
                                                        templateid,
                                                        inventory)

    print(output)

    output = zabbix.create_host('myhost',
                                interfaces,
                                groupid,
                                templateid,
                                inventory)


    output = zabbix.get_host('craphost')
    os.system('cls')
    pp = pprint.PrettyPrinter()
    pp.pprint(output)
