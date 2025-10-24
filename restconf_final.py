import json
import requests
requests.packages.urllib3.disable_warnings()

api_url = "https://10.0.15.61/"

headers = {'Content-Type': 'application/yang-data+json', 'Accept': 'application/yang-data+json' }
basicauth = ("admin", "cisco")

def rest_create():
    yangConfig = {
    "ietf-interfaces:interface": {
        "name": "Loopback66070221",
        "type": "iana-if-type:softwareLoopback",
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "172.2.21.1",
                    "netmask": "255.255.255.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }
}

    resp = requests.post(
        api_url + "restconf/data/ietf-interfaces:interfaces", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070221 is created successfully using Restconf"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot create: Interface loopback 66070221"


def rest_delete():
    resp = requests.delete(
        api_url + "restconf/data/ietf-interfaces:interfaces/interface=Loopback66070221", 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070221 is deleted successfully using Restconf"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot delete: Interface loopback 66070221"


def rest_enable():
    status_msg = rest_status()
    if "enable" in status_msg:
        return "Cannot enable: Interface loopback 66070221 (checked by Restconf)"
    else:
        yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback66070221",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True
        }
        }

        resp = requests.put(
            api_url + "restconf/data/ietf-interfaces:interfaces/interface=Loopback66070221", 
            data=json.dumps(yangConfig), 
            auth=basicauth, 
            headers=headers, 
            verify=False
            )

        if(resp.status_code >= 200 and resp.status_code <= 299):
            print("STATUS OK: {}".format(resp.status_code))
            return "Interface loopback 66070221 is enabled successfully using Restconf"


def rest_disable():
    status_msg = rest_status()
    if "disabled" in status_msg:
        return "Cannot shutdown: Interface loopback 66070221 (checked by Restconf)"
    else:
        yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback66070221",
            "type": "iana-if-type:softwareLoopback",
            "enabled": False
        }
        }

        resp = requests.put(
            api_url + "restconf/data/ietf-interfaces:interfaces/interface=Loopback66070221", 
            data=json.dumps(yangConfig), 
            auth=basicauth, 
            headers=headers, 
            verify=False
            )

        if(resp.status_code >= 200 and resp.status_code <= 299):
            print("STATUS OK: {}".format(resp.status_code))
            return "Interface loopback 66070221 is shutdowned successfully using Restconf"


def rest_status():
    api_url_status = "restconf/data/ietf-interfaces:interfaces-state/interface=Loopback66070221"

    resp = requests.get(
        api_url + api_url_status, 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}")
        response_json = resp.json()
        admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
        oper_status = response_json["ietf-interfaces:interface"]["oper-status"]
        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback 66070221 is enabled (checked by Restconf)"
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback 66070221 is disabled (checked by Restconf)"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}")
        return "No Interface loopback 66070221 (checked by Restconf)"
    else:
        print('Error. Status Code: {}')
