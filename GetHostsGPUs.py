#Get_Supported_GPUs

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
##   Description: Sample python code that retrives GPU information
##   from a cluster of VMware vSphere Hosts and display it on the
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
    TempHold = HostContent.viewManager.CreateContainerView(
        HostContent.rootFolder,[vim.HostSystem], True)
    for managed_object_ref in TempHold.view:
        print(managed_object_ref.name)
        try:
            if managed_object_ref.config.sharedPassthruGpuTypes:
                for GPU_Profile in managed_object_ref.config.sharedPassthruGpuTypes:
                    print(GPU_Profile)
            else:
                print("No GPUs found")
        except:
            print("Host not accessable")

###################################################
# End New Content
###################################################

    return 0
   

if __name__ == "__main__":
   main()
