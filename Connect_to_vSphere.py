

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
##   Description: Sample python code connects to a 
##   cluster of VMware vSphere Hosts and displays details on the
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

    HostContent=si.content
    print(HostContent)

    return 0
   

if __name__ == "__main__":
   main()
