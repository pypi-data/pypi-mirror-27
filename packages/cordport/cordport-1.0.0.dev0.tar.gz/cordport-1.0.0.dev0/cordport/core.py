import re
from functools import reduce
from subprocess import Popen, PIPE

class parser(object):
    def __init__(self, view=None, **kwargs):
        # OVS port command
        self.ovsname = "br-int"
        self.ovscmd = ["sudo", "ovs-ofctl", "dump-ports-desc"]
        self.ovscmd.append(self.ovsname)

        # Neutron port command
        self.neutroncmd = ["neutron", "port-list", "-f", "csv",
                           "-c", "id", "-c", "mac_address", "-c", "fixed_ips",
                           "--quote", "minimal"]

        self.parse()
        self.formatter(format_type=view)

    def parse(self):
        """
        ovs_: name with ovs's prefix, is the value of ovs bridge
        port_: name with port's prefix, is the value of neutron ports
        """

        p = Popen(self.ovscmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()

        # OVS regex pattern
        self.ovsports = dict()
        pattern = re.compile(r"(\d+)\(([0-9a-z\-]+)\): addr:([0-9a-f:]+)")

        # Parsing OVS port information
        for line in stdout.splitlines():
            match = pattern.search(line)
            if match:
                ovs_id, name, ovs_mac = match.groups(0)
                self.ovsports[ovs_mac] = {'ovs_id': ovs_id, 'name': name}

        p = Popen(self.neutroncmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()

        # Neutron port regex pattern
        self.ntports = dict()
        pattern = re.compile("([0-9a-f\-]{36}),([0-9a-f:]+),.+"
                              "([0-9a-f\-]{36}).+\"(\d+\.\d+\.\d+\.\d+).*")

        # Parsing Neutron port information
        for line in stdout[1:].splitlines():
            match = pattern.search(line)
            if match:
                port_id, port_mac, net_id, port_ip = match.groups(0)
                self.ntports[port_mac] = {'id': port_id,
                                          'net_id': net_id, 'port_ip': port_ip}

    def port_match(self, mac):
        """
        return: mac(string), port/ovs(dict)
        """

        if mac in self.ovsports:
            for port_mac, port in self.ntports.items():
                if mac[6:] == port_mac[6:]:
                    return port_mac, port

        elif mac in self.ntports:
            for ovs_mac, ovs in self.ovsports.items():
                if mac[6:] == ovs_mac[6:]:
                    return ovs_mac, ovs

        return "None", None

    def formatter(self, format_type="ovs"):
        def natural_keys(text):
            if "." in text:
                ip = text.split(":")[0].split(".")
                return reduce(lambda a, b: (a << 8) + b, map(int, ip), 0)
            else:
                return int(text.split(":")[0])

        OVS_VIEW = "{ovs_id}:\t{name} ({ovs_mac}) -> {port_ip} ({port_mac})"
        VM_VIEW = "{port_ip}: {ovs_name} ({ovs_mac})"

        views = {
            'ovs': OVS_VIEW,
            'vm': VM_VIEW
        }

        view = views[format_type]
        out = list()

        if format_type == "ovs":
            for ovs_mac, ovs in self.ovsports.items():
                port_mac, port = self.port_match(ovs_mac)
                port_ip = port['port_ip'] if port else "None"

                out.append(view.format(ovs_id=ovs['ovs_id'], name=ovs['name'],
                                       ovs_mac=ovs_mac, port_ip=port_ip,
                                       port_mac=port_mac))

        elif format_type == "vm":
            for port_mac, port in self.ntports.items():
                ovs_mac, ovs = self.port_match(port_mac)
                ovs_name = ovs['name'] if ovs else "None"

                out.append(view.format(port_ip=port["port_ip"],
                                       ovs_name=ovs_name, ovs_mac=ovs_mac))

        print('\n'.join(sorted(out, key=natural_keys)))

