#Get_VMs_w_vGPUs

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
##   Description: Sample python code that retrives vGPU information
##   from a cluster of VMware vSphere Hosts and displays it on the
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

def main():
    context = None
    if hasattr(ssl, '_create_unverified_context'):
        context = ssl._create_unverified_context()
    si = SmartConnect(host="vsa01.wondernerd.local",
                        user="administrator@wondernerd.local",
                        pwd="Kansas17-7",
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

    DataCenterContent = HostContent.rootFolder.childEntity[0] #Assume single DC
    VMs = DataCenterContent.vmFolder.childEntity
    for i in VMs:
        #print("VM Name: "+ i.name)

        if isinstance(i,vim.Folder):
            #**************found a folder***************
            for ChildVM in i.childEntity:
                
                # Does it have a vGPU
                for VMVirtDevice in ChildVM.config.hardware.device:
                    if isinstance(VMVirtDevice, vim.VirtualPCIPassthrough) and \
                        hasattr(VMVirtDevice.backing, "vgpu"):
                        print("VM Name: "+ ChildVM.name)
                        print("In Folder: "+ ChildVM.parent.name)
                        print("Device Backing: " + VMVirtDevice.backing.vgpu)
                        print("Device Label: " + VMVirtDevice.deviceInfo.label)
                        print("Device Summary: " + VMVirtDevice.deviceInfo.summary)
                        print("*************************************")
        #print(i.parent.name)
        #print(i.childType)
        
###################################################
# End New Content
###################################################

    return 0
   

if __name__ == "__main__":
   main()
