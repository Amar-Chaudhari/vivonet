import httplib
import json

from main.models import *

class ComputeAndPush(object):
    def __init__(self, server, srcname, dstname, intent):
        self.server = server
        self.srcname = srcname
        self.dstname = dstname
        self.intent = intent

    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])

    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200

    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200

    def rest_call(self, data, action, path):
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        conn.close()
        return ret

    def get_endpoints(self):
        """ To get dpid, endport and ip address of PE router"""

        src_switch = None
        dst_switch = None
        path = '/wm/device/'
        endpoints = []  # List to store endpoint information
        ret = self.rest_call({}, 'GET', path)
        output = json.loads(ret[2])  # Since path is not json, this string needs to be converted to json.
        devices = output['devices']  # Single key in dict output which contains a list of endpoints
        src_host = Customer.objects.get(location=self.srcname).Connected_Host
        dst_host = Customer.objects.get(location=self.dstname).Connected_Host
        for i in xrange(0, len(devices)):
            ip = output['devices'][i]['ipv4'][0]
            if ip == src_host:
                src_switch = output['devices'][i]['attachmentPoint'][0]['switch']
            elif ip == dst_host:
                dst_switch = output['devices'][i]['attachmentPoint'][0]['switch']
            endport = output['devices'][i]['attachmentPoint'][0]['port']
            endpoints.append({
                'src_switch': src_switch,
                'dst_switch': dst_switch,
                'endport': endport,
                'ip': ip,
            })
        print endpoints
        return endpoints

    def find_path(self):
        """To find path as per the required intent"""

        endpoints = self.get_endpoints()
        for endpoint in endpoints:
            if endpoint['src_switch'] is not None:
                srcdpid = endpoint['src_switch']
            if endpoint['dst_switch'] is not None:
                dstdpid = endpoint['dst_switch']
        path = '/wm/routing/paths/fast/{}/{}/2/json'.format(srcdpid, dstdpid)
        ret = self.rest_call({}, 'GET', path)
        output = json.loads(ret[2])
        lat1 = output['results'][0]['latency']
        lat2 = output['results'][1]['latency']
        hop1 = output['results'][0]['hop_count']
        hop2 = output['results'][1]['hop_count']
        if self.intent == "least latency":
            if lat1 <= lat2:
                path = output['results'][0]['path']
            else:
                path = output['results'][1]['path']
        if self.intent == "least hop count":
            if hop1 <= hop2:
                path = output['results'][0]['path']
            else:
                path = output['results'][1]['path']
        return path

    def construct_flows(self):
        """To construct flows from various data in the required path"""

        flows = []
        path = self.find_path()
        in_hop = path[0]
        out_hop = path[-1]

        endpoints = self.get_endpoints()  # Find outgoing ports for endpoints and enter in flow dict
        for endpoint in endpoints:
            if endpoint['src_switch'] is not None:
                in_hop['in_port'] = endpoint['endport']
            if endpoint['dst_switch'] is not None:
                out_hop['actions'] = 'output=' + endpoint['endport']

        in_hop['actions'] = 'output=' + in_hop.pop('port')
        out_hop['in_port'] = out_hop.pop('port')
        flows.extend([in_hop, out_hop])

        int_path = path[1:-1]  # Intermediate path, excluding source and destination ovs
        for i in range(0, len(int_path), 2):  # Formatting
            int_path[i]['in_port'] = int_path[i].pop('port')
            int_path[i]['switch'] = int_path[i].pop('dpid')
            int_path[i + 1]['switch'] = int_path[i + 1].pop('dpid')
            int_path[i + 1]['actions'] = int_path[i + 1].pop('port')
            int_path[i + 1]['actions'] = 'output={}'.format(int_path[i + 1]['actions'])
            int_path[i].update(int_path[i + 1])
            flows.append(int_path[i])
        return flows

    def create_flows(self):
        """Create final flows"""

        src_prefix = Customer.objects.get(location=self.srcname).Prefix
        dst_prefix = Customer.objects.get(location=self.dstname).Prefix
        flows = self.construct_flows()
        # Add additional fields in the flow
        req_fields = {
            'name': 'flow_mod_{}'.format(self.intent),
            'cookie': None,
            'priority': 32768,
            'active': 'true',
            'src-ip': src_prefix,
            'dst-ip': dst_prefix,
        }
        for switch in flows:
            switch.update(req_fields)
        for switch in flows:  # Human readable output
            print
            for key, value in switch.items():
                print key, value
        return flows

    def push_flows(self):
        flows = self.create_flows()
        for flow in flows:
            self.set(flow)


if __name__ == '__main__':
    c = ComputeAndPush('198.11.21.36', 'DEN', 'SFO', 'least latency')
    c.create_flows()
