#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: aci_get_interface
short_description: Get interface data on Cisco ACI fabrics
description:
- Get interface data on Cisco ACI fabrics
author:
- Chris Gascoigne (@chrisgascoigne)
version_added: '2.4'
requirements:
    - ACI Fabric 1.0(3f)+
options:
    host:
        description:
            - IP Address or hostname of APIC resolvable by Ansible control host
        required: true
    username:
        description:
            - Username used to login to the switch
        required: true
        default: 'admin'
    password:
        description:
            - Password used to login to the switch
        required: true
    protocol:
        description:
            - Dictates connection protocol to use
        default: https
        choices: ['http', 'https']
'''

EXAMPLES = r'''
- aci_get_interface:
    host: "{{ host }}"
    username: "{{ user }}"
    password: "{{ pass }}"
    protocol: "{{ protocol }}"
    interface: "topology/pod-1/paths-122/pathep-[eth1/2]"
    
- aci_get_interface:
    host: "{{ host }}"
    username: "{{ user }}"
    password: "{{ pass }}"
    protocol: "{{ protocol }}"
    interface: "topology/pod-1/paths-122/extpaths-101/pathep-[eth1/2]"
'''

from ansible.module_utils.aci import ACIModule, aci_argument_spec
from ansible.module_utils.basic import AnsibleModule
import json
import re


results = {}
def set_fact(fact, value):
    if 'anisble_facts' not in results:
        results['ansible_facts'] = {}
    results['ansible_facts'][fact]=value
    
    
def get_epgs(interface, aci, module):
    #interface should be of form topology/pod-1/paths-122/pathep-[eth1/2]
    query_str = '/api/class/fvRsPathAtt.json?query-target-filter=eq(fvRsPathAtt.tDn,"{}")'.format(interface)
    interface_epgs = []
    try:
        query_res = json.loads(aci.query(query_str))
        for rspathatt in query_res:
            epg = {}
            epg['interface'] = interface
            epg['encap'] = rspathatt['fvRsPathAtt']['attributes']['encap']
            epg['mode'] = rspathatt['fvRsPathAtt']['attributes']['mode']
            epg['dn'] = re.match(r'^uni/(tn-[a-zA-Z0-9\-]+/ap-[a-zA-Z0-9\-]+/epg-[a-zA-Z0-9\-]+)', rspathatt['fvRsPathAtt']['attributes']['dn']).groups()[0]
            interface_epgs.append(epg)
    except Exception as e:
        module.fail_json(msg="Error occured retrieving path info: %s"%e, **results)
        
    return interface_epgs

def main():
    argument_spec = aci_argument_spec
    argument_spec.update(
        interface=dict(type='str', required=True, aliases=['contract_name', 'name'])
    )
    
    module = AnsibleModule(
            argument_spec=argument_spec,
            supports_check_mode=True
    )
    
    interface = module.params['interface']
    
    aci = ACIModule(module)
    # query_str = '/api/class/infraRsHPathAtt.json?query-target-filter=eq(infraRsHPathAtt.tDn,"{}")&target-subtree-class=relnTo'.format(interface)
    # try:
    #     query_res = json.loads(aci.query(query_str))
    #     if len(query_res) == 0:
    #         module.fail_json(msg="Interface not found", **results)
    #     int_override_dn = query_res[0]['infraRsHPathAtt']['attributes']['dn']
    # except Exception as e:
    #     module.fail_json(msg="Error occured retrieving path info: %s"%e, **results)
    #
    #
    #
    # set_fact('int_override_dn', int_override_dn)
    
    set_fact('interface_epgs', get_epgs(interface, aci, module))
    
    results['changed'] = False
    
    module.exit_json(**results)
    
if __name__=="__main__":
    main()