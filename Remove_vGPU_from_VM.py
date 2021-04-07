#Remove_vGPU_From_VM

###################################################################
##   Copyright 2021 Anthony Foster
##
##   Licensed under the Apache License, Version 2.0 (the "License");
##   you may not use this file except in compliance with the License.
##   You may obtain a copy of the License at
##
##       http://www.apache.org/licenses/LICENSE-2.0
##
##   Unless required by applicable law or agreed to in writing, software
##   distributed under the License is distributed on an "AS IS" BASIS,
##   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##   See the License for the specific language governing permissions and
##   limitations under the License.
###################################################################

###################################################################
##   Description: Sample python code that adds a vGPU to a VM
##   in a cluster of VMware vSphere Hosts and displays it on the
##   screen. This was developed for use as part of a GTC21 session
###################################################################




from __future__ import print_function
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
from pyVmomi import vmodl

import argparse
import atexit
import getpass
import ssl
from pyVim.task import WaitForTask

def main():
    context = None
    if hasattr(ssl, '_create_unverified_context'):
        context = ssl._create_unverified_context()
    si = SmartConnect(host="[VCSA/Host NAME or IP HERE]",
                        user="[USER NAME HERE]",
                        pwd="[PASSWORD HERE]",
                        port=443,
                        sslContext=context)
    if not si:
        print("Could not connect to the specified host using specified "
             "username and password")
        return -1

    atexit.register(Disconnect, si)

###################################################
# New Content
###################################################

    HostContent=si.content

    vm = None
    vGPUobj = None
    TempVMlist = HostContent.viewManager.CreateContainerView(HostContent.rootFolder,\
        [vim.VirtualMachine], True)
    for managed_VM_ref in TempVMlist.view: #Go thought VM list
        if managed_VM_ref.name == "Compute000": #find Desired VM
            print(managed_VM_ref)
            print(managed_VM_ref.name)
            vm = managed_VM_ref #Capture VM as an obj to use next
    if vm != None: #Safety to make sure not added to null object
        for VMVirtDevice in vm.config.hardware.device: #Go through vPCI and find vGPU
            if isinstance(VMVirtDevice, vim.VirtualPCIPassthrough) and \
                hasattr(VMVirtDevice.backing, "vgpu"):
                if VMVirtDevice.backing.vgpu == "grid_p4-4q":
                    vGPUobj = VMVirtDevice
                    print("Found vGPU: " + VMVirtDevice.backing.vgpu)

        cspec = vim.vm.ConfigSpec()
        cspec.deviceChange = [vim.VirtualDeviceConfigSpec()]
        cspec.deviceChange[0].operation = 'remove'
        cspec.deviceChange[0].device = vGPUobj
        WaitForTask(vm.Reconfigure(cspec))
        print("Removed vGPU")

        
###################################################
# End New Content
###################################################

    return 0
   

if __name__ == "__main__":
   main()
