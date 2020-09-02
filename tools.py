"""Tools module for Main Program"""
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

import json
import requests
import warnings
import ipaddress
import sys
import csv
import re
import os
import logging

requests.packages.urllib3.disable_warnings()

def _get(uri,username,password,HEADERS):
    try:
        response = requests.get(url=uri, auth=(username,password), headers=HEADERS, verify=False, timeout=5)
    except requests.exceptions.Timeout as e: 
        print()
        print("+-----------------------------+")
        print("Error Connection Timeout")
        print("+-----------------------------+")
        sys.exit()
    
    if response.ok:
        data = response.json()
    else:
        data = response.status_code
    return data

def _delete(uri,username,password,HEADERS,endpoint_id):
    response = requests.delete(url=uri + endpoint_id, auth=(username,password), headers=HEADERS, verify=False)
    return response.status_code

def _put(uri,username,password,HEADERS,payload):
    response = requests.put(url=uri, auth=(username,password), headers=HEADERS, data=payload, verify=False)
    return response.status_code

def verify_mac(mac):
    if mac and re.search(r'([0-9A-F]{2}[:]){5}([0-9A-F]){2}', mac.upper()) is not None:
        return True
    else:
        return False

def get_endpoint_id(uri,mac,username,password,HEADERS):
    url = uri + "endpoint/name/" + mac
    data = _get(url,username,password,HEADERS)
    if data == 404:
        endpoint_id = None
    elif data == 401 or data == 403:
        sys.exit("Credentials are invalid\n")
    elif data == 400:
        sys.exit("Bad Request, please verify IP Address\n")    
    else:        
        endpoint_id = data.get("ERSEndPoint").get("id")
    return endpoint_id

def get_endpoint_group(uri,mac,username,password,HEADERS):
    url = uri + "endpoint/name/" + mac
    data = _get(url,username,password,HEADERS)
    if data == 404:
        endpoint_id = None
    elif data == 401 or data == 403:
        sys.exit("Credentials are invalid\n")
    elif data == 400:
        sys.exit("Bad Request, please verify IP Address\n")    
    else:        
        endpoint_id = data.get("ERSEndPoint").get("groupId")
    return endpoint_id

def get_groupendpoint_id(uri,username,password,HEADERS):
    data = _get(uri,username,password,HEADERS)
    if data == 404:
        groupendpoint_id = None
    elif data == 401 or data == 403:
        sys.exit("Credentials are invalid\n")
    elif data == 400:
        sys.exit("Bad Request, please verify IP Address\n")    
    else:        
        groupendpoint_id = data.get("EndPointGroup").get("id")
    return groupendpoint_id

def open_csv(filepath):
    try:
        with open(os.path.expanduser(filepath), newline="") as csvfile:
            csv_content = list(csv.DictReader(csvfile))
            if not csv_content:
                sys.exit(f"File '{filepath}' is empty")
            else:
                return csv_content    

    except OSError as e:
        print(e)
        sys.exit(f"File '{filepath}' was not found!")

def is_valid_ip(ipv4):
    """Tests to see if provided value is valid IPv4 or IPv6."""
    try:
        ipaddress.ip_address(ipv4)
    except ValueError:
        return False
    else:
        return True