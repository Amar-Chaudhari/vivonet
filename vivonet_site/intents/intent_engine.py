import httplib
import json

from main.models import *
from datetime import datetime
import re

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
        path = '/wm/staticentrypusher/json'
        ret = self.rest_call(data, 'POST', path)
        return ret

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
            if ip == dst_host:
                dst_switch = output['devices'][i]['attachmentPoint'][0]['switch']
            endport = output['devices'][i]['attachmentPoint'][0]['port']
            endpoints.append({
                'src_switch': src_switch,
                'dst_switch': dst_switch,
                'endport': endport,
                'ip': ip,
            })
        
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
        if self.intent == "least_latency":
            if lat1 <= lat2:
                path = output['results'][0]['path']
            else:
                path = output['results'][1]['path']
        if self.intent == "least_hop_count":
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
        in_hop['switch'] = str(in_hop.pop('dpid'))
        out_hop = path[-1]
        out_hop['switch'] = str(out_hop.pop('dpid'))

        endpoints = self.get_endpoints()  # Find outgoing ports for endpoints and enter in flow dict
        for endpoint in endpoints:
            if endpoint['src_switch'] is not None:
                in_hop['in_port'] = str(endpoint['endport'])
            if endpoint['dst_switch'] is not None:
                out_hop['actions'] = 'output={}'.format(endpoint['endport'])

        in_hop['actions'] = 'output={}'.format(in_hop.pop('port'))
        out_hop['in_port'] = str(out_hop.pop('port'))
        flows.extend([in_hop, out_hop])

        int_path = path[1:-1]  # Intermediate path, excluding source and destination ovs
        for i in range(0, len(int_path), 2):  # Formatting
            int_path[i]['in_port'] = str(int_path[i].pop('port'))
            int_path[i]['switch'] = str(int_path[i].pop('dpid'))
            int_path[i + 1]['switch'] = str(int_path[i + 1].pop('dpid'))
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
            "priority": "32768",
            "active": "true",
            "ipv4_src": str(src_prefix),
            "ipv4_dst": str(dst_prefix),
	        "eth_type": "0x800"
        }
        for switch in flows:
            switch["name"] = "{}_{}_{}_{}".format(self.intent, switch['switch'], self.srcname, self.dstname)
            switch.update(req_fields)

        return flows

    def push_flows(self):
        """Push flows to the required switches"""

        flows = self.create_flows()
        result = [self.set(flow) for flow in flows]
        return result

    def verify_push(self):
        """Verify push operation"""

        response = self.push_flows()
        result = [False for code in response if code[0] != 200]
        return False if False in result else True

    def add_intent_data(self):
        """Add intent information to database. Returns path taken by the intent"""

        if self.verify_push():
            src_prefix = Customer.objects.get(location=self.srcname).Prefix
            dst_prefix = Customer.objects.get(location=self.dstname).Prefix
            path = self.find_path()
            dpid = []
            for hop in path:
                if hop['dpid'] not in dpid:
                    dpid.append(hop['dpid'])

            Intent_Data.objects.create(From_Location=self.srcname,
                                            To_Location=self.dstname,
                                            Intent_Type=self.intent,
                                            Source_IP=src_prefix,
                                            Destination_IP=dst_prefix,
                                            Path=dpid,
                                            timestamp=datetime.now())
            return dpid
        else:
            return False

    def add_intent_path_data(self):
        """Add actual intent path to database"""

        dpids_list = self.add_intent_data()
        if dpids_list is not False:
            path = Intent_Data.objects.get(Path=dpids_list)
            intent = path.Intent_Type

            dpids = dpids_list.split('-')
            for switch in dpids:
                call = '/wm/staticflowpusher/list/{}/json'.format(switch)
                ret = self.rest_call({}, 'GET', call)
                flows = json.loads(ret[2])[switch]
                for flow in flows:
                    for name in flow.keys():
                        flow_intent = re.search('(.*?)_\d', name)
                        if flow_intent is not None:
                            if intent == flow_intent.group(1):
                                Intent_Path_Data.objects.create(Path_id=path.id,
                                                                switch=switch,
                                                                name=name,
                                                                cookie=flow[name]['cookie'],
                                                                priority=flow[name]['priority'],
                                                                active='True',
                                                                ipv4_src=flow[name]['match']['ipv4_src'],
                                                                ipv4_dst=flow[name]['match']['ipv4_dst'],
                                                                in_port=flow[name]['match']['in_port'],
                                                                actions=flow[name]['instructions']['instruction_apply_actions']['actions'])

            return True
        else:
            return False

    def intentEngine(self):
        return self.add_intent_path_data()

if __name__ == '__main__':
    c = ComputeAndPush('198.11.21.36', 'DEN', 'SFO', 'least_latency')
    c.create_flows()
