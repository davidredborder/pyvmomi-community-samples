#!/usr/bin/env python
# VMware vSphere Python SDK
# Copyright (c) 2008-2021 VMware, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Python program for listing the VMs on an ESX / vCenter host
"""

import re
from pyVmomi import vmodl, vim
from tools import cli, service_instance


def print_vm_info(virtual_machine):
    """
    Print information for a particular virtual machine or recurse into a
    folder with depth protection
    """
    summary = virtual_machine.summary
    #print("Name       : ", summary.config.name)
    #print("State      : ", summary.runtime.powerState)
    print(f'{summary.config.name:30} ==> {summary.runtime.powerState:5}')


def main():
    """
    Simple command-line program for listing the virtual machines on a system.
    """

    parser = cli.Parser()
    parser.add_custom_argument('-f', '--find', required=False,
                               action='store', help='String to match VM names')
    parser.add_custom_argument('-v', '--vm-name', required=False, action='store',
                               help='Exact names of the Virtual Machines to filter')
    args = parser.get_args()
    si = service_instance.connect(args)

    try:
        vmnames = args.vm_name
        content = si.RetrieveContent()

        container = content.rootFolder  # starting point to look into
        view_type = [vim.VirtualMachine]  # object types to look for
        recursive = True  # whether we should look into it recursively
        container_view = content.viewManager.CreateContainerView(
            container, view_type, recursive)

        children = container_view.view
        if args.find is not None:
            pat = re.compile(args.find, re.IGNORECASE)
        for child in children:
            if args.find is None and args.vm_name is None:
                print_vm_info(child)
            else:
                if args.find:
                    if pat.search(child.summary.config.name) is not None:
                        print_vm_info(child)
                else:
                    if child.summary.config.name in vmnames: print_vm_info(child)

    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1

    return 0


# Start program
if __name__ == "__main__":
    main()
