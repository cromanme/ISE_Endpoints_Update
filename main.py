# -*- coding: utf-8 -*-
__author__ = "Christian Méndez Murillo"
__email__ = "cmendezm@cisco.com"
__copyright__ = """
Copyright 2020, Cisco Systems, Inc. 
All Rights Reserved. 
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
OTHER DEALINGS IN THE SOFTWARE. 
"""
__status__ = "Development"  # Prototype, Development or Production

import sys
import logging
from getpass import getpass
import tools

logging.basicConfig(filename='app.log', 
                    filemode='w', 
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


print()
ise_host = "10.122.176.10"
ise_user = "admin"
ise_passwd = "Ise1234!"
option = input("Type 1 to remove association\nType 2 to restore association\nOption: ")

if option == "1" or option == "2":
    print()
else:
    sys.exit(f"Invalid input detected. Terminating Script")


HEADERS = {
        'Accept': "application/json",
        'Content-Type': "application/json",
}
filename = "csv/endpoints.csv"
uri = "https://"+ise_host+":9060/ers/config/"

print()
if not tools.is_valid_ip(ise_host):
    sys.exit(f"Invalid IP Address: '{ise_host}'")

data = tools.open_csv(filename)

for row in data:
    mac = row["MAC"]
    group = row["GroupID"]
    if tools.verify_mac(mac):
        endpoint_id = tools.get_endpoint_id(uri,mac,ise_user,ise_passwd,HEADERS)
        endpoint_group_id = tools.get_endpoint_group(uri,mac,ise_user,ise_passwd,HEADERS)
    else:
        print("Invalid MAC Address")
        continue
    if endpoint_id:
        url = uri + "endpointgroup/name/" + group
        group_id =  tools.get_groupendpoint_id(url,ise_user,ise_passwd,HEADERS)
        if group_id:
            if option == "1":
                if group_id == endpoint_group_id:
                    payload = "{\n    \"ERSEndPoint\": {\n        \"staticGroupAssignment\": false\n    }\n}"
                    url = uri + "endpoint/" + endpoint_id
                    if tools._put(url,ise_user,ise_passwd,HEADERS,payload) == 200:
                        print("Succcesfully updated MAC Address: ",mac)
                    else:
                        print("Error updating MAC Address: ",mac)
                else:
                    print("MAC Address: ",mac + " is not part of Group: ",group)
            elif option == "2":
                if group_id != endpoint_group_id:
                    payload = "{\n    \"ERSEndPoint\": {\n        \"staticGroupAssignment\": true,\n        \"groupId\": \""+group_id+"\"\n    }\n}"
                    url = uri + "endpoint/" + endpoint_id
                    if tools._put(url,ise_user,ise_passwd,HEADERS,payload) == 200:
                        print("Succcesfully updated MAC Address: ",mac)
                    else:
                        print("Error updating MAC Address: ",mac)
                else:
                    print("MAC Address: ",mac + " is already part of Group: ",group)        
        else:
            print("Endpoint Identity Group:",group + " Not Found!!!")
    else:
        print("MAC Address:",mac," is not in the database")
print("\nScript completed successfully\n")
