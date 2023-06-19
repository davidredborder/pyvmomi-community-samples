#!/usr/bin/env python
# Copyright (c) 2015 Christian Gerbrandt <derchris@derchris.eu>
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
Python port of William Lam's generateHTML5VMConsole.pl
Also ported SHA fingerprint fetching to Python OpenSSL library
"""

import ssl
import time
import OpenSSL
from pyVmomi import vim
from tools import cli, service_instance


def get_vm(content, name):
    try:
        name = str(name)
    except TypeError:
        pass

    vm = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True)

    for vm_obj in container.view:
        if vm_obj.name == name:
            vm = vm_obj
            break
    return vm


def main():
    """
    Simple command-line program to get the moid
    Can be used to start vmrc and open the screen of the vm
    """

    parser = cli.Parser()
    parser.add_required_arguments(cli.Argument.VM_NAME)
    args = parser.get_args()
    si = service_instance.connect(args)

    content = si.RetrieveContent()

    vm = get_vm(content, args.vm_name)
    vm_moid = vm._moId
    print(vm._moId)

# Start program
if __name__ == "__main__":
    main()
