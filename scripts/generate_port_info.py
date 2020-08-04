#!/usr/bin/python3

import os
import json
import re

output = '---\ntrunks:'

trunk_ports_list = []
unused_ports_list = []
management_interface = 'GigabitEthernet0/0'

regex = re.compile(r'Gig \d/\d')

for subdir, dirs, files in os.walk('temp'):
    for d in dirs:
        for subdir1, dirs1, files1 in os.walk(f'{subdir}/{d}'):
            for file in files1:
                if 'interfaces' in file:
                    with open(f'temp/{d}/{file}') as f:
                        data = json.loads(f.read()).keys()

                        # Generate Unused Ports List
                        for unused_port in data:
                            unused_ports_list.append(unused_port)

                else:
                    with open(f'temp/{d}/{file}') as f:
                        data = json.loads(f.read())

                        # Generate Trunk Ports List
                        for line in data:
                            port = regex.search(line).group(0).replace('Gig ', 'GigabitEthernet')
                            trunk_ports_list.append(port)

            # Remove Duplicate Ports in List
            trunk_ports_list = list(dict.fromkeys(trunk_ports_list))
            unused_ports_list = list(dict.fromkeys(unused_ports_list))

            # Remove Management Port From Lists
            if management_interface in trunk_ports_list:
                trunk_ports_list.remove(management_interface)
            if management_interface in unused_ports_list:
                unused_ports_list.remove(management_interface)

            # Add Trunk Ports to Output File
            for trunk_port in trunk_ports_list:
                output += f'\n  - {trunk_port}'

            # Start of Unused Ports File Section
            output += '\nunused_ports:'

            # Add Unused Ports to Output File
            for unused_port in unused_ports_list:
                if unused_port not in trunk_ports_list:
                    output += f'\n  - {unused_port}'

            # Write File
            with open(f"host_vars/{file.split('_')[0]}.yml", 'w') as output_file:
                output_file.write(output)

            # Reset To Write Another File
            output = '---\ntrunks:'
            trunk_ports_list = []
            unused_ports_list = []
