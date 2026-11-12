import socket, json, tls_client
from core.modules.networking.port_scan import scan
from core.modules.networking.attacks import ftp_attack
from core.modules.logging import *
from core.modules.general import flatten_results

class Networking:
    def __init__(self, host):
        self.host   = host
        self.report = {}

        self.session = tls_client.Session()

        self.port_attacks = {
            "21" : ftp_attack
        }

        self.domain_host_check()

    def domain_host_check(self):
        info("Determining host type")
        basic = socket.gethostbyname(self.host)
        self.report["basic"] = {}
        if str(basic) == self.host:
            self.report["basic"]["handed"] = "IP"
            self.report["basic"]["ip"]     = self.host
            self.report["basic"]["domain"] = socket.gethostbyaddr(self.host)[0]
        else:
            self.report["basic"]["handed"] = "DOMAIN"
            self.report["basic"]["ip"]     = socket.gethostbyname(self.host)
            self.report["basic"]["domain"] = self.host
        success("Determined host type!")

    def ip_lookup(self):
        api = "http://ip-api.com/json/{}".format(self.report["basic"]["ip"])

        response = self.session.get(api)
        data = response.json()

        self.report["ip_lookup"] = data

    def run(self):
        print()
        info("Looking up IP...")
        self.ip_lookup()
        success("Completed IP lookup!")

        print()

        info("Scanning port...")
        scan(self.report["basic"]["ip"], self.report)
        success("Port scan finished!")

        print()

        if self.report["ports"]:
            info("Probing open ports...")
            for port in self.report["ports"]:
                if port in self.port_attacks:
                    func = self.port_attacks[port]

                    response = func(self.report["basic"]["ip"])

                    self.report["ports"][port]["extra"] = response
            success("Probed ports!")
        print(self.report)
        print()
        return self.report