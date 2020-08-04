#! /usr/bin/python3

from jinja2 import Environment, FileSystemLoader
import yaml

ENV = Environment(loader=FileSystemLoader('templates'))
ENV.trim_blocks = True
ENV.lstrip_blocks = True

template = ENV.get_template('vlan.j2')

vlan_list = []

# Generate list of VLAN information
for vlan in range(5, 501, 5):
    vlan_list.append({'name': f'VLAN_{vlan}', 'id': vlan})

# Create group var file with template and vlan list
with open('group_vars/switches.yml', 'w') as f:
    f.write(template.render(vlans=vlan_list))
