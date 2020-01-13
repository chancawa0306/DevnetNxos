import requests
import json
from ncclient import manager
import sys
from lxml import etree

"""
Modify these please
"""
def task1():

    switchuser='admin'
    switchpassword='cisco'

    url='http://10.75.37.244/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "interface loopback1",
          "version": 1
        },
        "id": 1
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "ip add 1.1.1.1/32",
          "version": 1
        },
        "id": 2
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "no shut ",
          "version": 1
        },
        "id": 3
      }
    ]
    response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
    print("\nNow finish adding Loopback 1 with IP address 1.1.1.1/32 \n")
    print(response[0])

def task2():
    sys.path.append("..")  # noqa

    device = {
        "address": "10.75.37.244",
        "netconf_port": 830,
        "restconf_port": 443,
        "ssh_port": 22,
        "username": "admin",
        "password": "cisco"
    }

    # Loopback Info - Change the details for your interface
    loopback = {"id": "2", "ip": "2.2.2.2/32"}

    add_ip_interface = """<config>
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
        <intf-items>
            <lb-items>
                <LbRtdIf-list>
                    <id>lo{id}</id>
                    <adminSt>up</adminSt>
                    <descr>Full intf config via NETCONF</descr>
                </LbRtdIf-list>
            </lb-items>
        </intf-items>
        <ipv4-items>
            <inst-items>
                <dom-items>
                    <Dom-list>
                        <name>default</name>
                        <if-items>
                            <If-list>
                                <id>lo{id}</id>
                                <addr-items>
                                    <Addr-list>
                                        <addr>{ip}</addr>
                                    </Addr-list>
                                </addr-items>
                            </If-list>
                        </if-items>
                    </Dom-list>
                </dom-items>
            </inst-items>
        </ipv4-items>
    </System>
    </config>""".format(id=loopback["id"], ip=loopback["ip"])
    #print(add_ip_interface)

    with manager.connect(host=device["address"],
                         port=device["netconf_port"],
                         username=device["username"],
                         password=device["password"],
                         hostkey_verify=False) as m:
        # Add the loopback interface
        print("\nNow adding Loopback {} IP address {} to device {}...\n".format(loopback["id"], loopback["ip"],
                                                                                 device["address"]))
        netconf_response = m.edit_config(target='running', config=add_ip_interface)
        # Parse the XML response
        print(netconf_response)

task1()
task2()