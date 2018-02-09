import requests
import json


class StaticEntryPusher(object):
    def __init__(self, server):
        self.server = server

    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return ret

    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret

    def remove(self, data):
        ret = self.rest_call(data, 'DELETE')
        return ret

    def rest_call(self, data, action):
        content = False
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }
        body = json.dumps(data)
        if action == "GET":
            conn = requests.get(self.server+"/wm/staticentrypusher/list/all/json",headers=headers)
        elif action == "POST":
            conn = requests.post(self.server+"/wm/staticentrypusher/json",headers=headers,data=body)
        elif action == "DELETE":
            conn = requests.delete(self.server+"/wm/staticentrypusher/json",headers=headers,data=body)

        if conn.status_code == 200:
            print(conn.status_code)
            content = conn.content
        conn.close()
        return content


pusher = StaticEntryPusher('http://198.11.21.36:8080')


flow1_1 = {
    'switch': "00:00:00:0c:29:69:ca:2e",
    "name": "flow_mod_1_1",
    "cookie": "0",
    "priority": "32768",
    "in_port": "3",
    "active": "true",
    "eth_type":"0x0800",
    "eth_src":"00:0c:29:f9:6c:f7",
    "eth_dst":"00:0c:29:b1:64:a3",
    "ipv4_src":"20.0.0.1",
    "ipv4_dst":"20.0.0.2",
    "actions":"set_field=eth_dst->00:0c:29:b1:64:a3,output=1"
}

flow1_2 = {
    'switch': "00:00:00:0c:29:15:ab:33",
    "name": "flow_mod_1_2",
    "cookie": "0",
    "priority": "32768",
    "in_port": "1",
    "active": "true",
    "eth_type":"0x0800",
    "eth_src":"00:0c:29:f9:6c:f7",
    "eth_dst":"00:0c:29:b1:64:a3",
    "ipv4_src":"20.0.0.1",
    "ipv4_dst":"20.0.0.2",
    "actions":"set_field=eth_dst->00:0c:29:b1:64:a3,set_field=ipv4_dst->20.0.0.2,output=3"
}


flow1_3 = {
    'switch': "00:00:00:0c:29:d9:97:e3",
    "name": "flow_mod_1_3",
    "cookie": "0",
    "priority": "32768",
    "in_port": "1",
    "active": "true",
    "eth_type":"0x0800",
    "eth_src":"00:0c:29:f9:6c:f7",
    "eth_dst":"00:0c:29:b1:64:a3",
    "ipv4_src":"20.0.0.1",
    "ipv4_dst":"20.0.0.2",
    #"actions":"set_field=eth_dst->00:0c:29:b1:64:a3,set_field=ipv4_dst->20.0.0.2,output=3"
    "actions":"output=all"
}

print(pusher.remove(flow1_1))
print(pusher.remove(flow1_2))
print(pusher.remove(flow1_3))
print(pusher.get(""))
