import socket, whois, tls_client
from core.modules.networking.port_scan import scan
from core.modules.networking.attacks import ftp_attack
from core.modules.networking.check_vpn import vpn
from core.modules.logging import *

class Networking:
    def __init__(self, host):
        self.host   = host
        self.report = {}

        self.session = tls_client.Session()

        self.port_attacks = {
            "21" : ftp_attack
        }

    def is_valid(self):
        try:
            socket.gethostbyname(self.host)
            return True
        except:
            return False

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

    def whois_(self):
        lookup = whois.whois(self.report["basic"]["domain"])

        self.report["whois"] = {
            "basic" : {
                "registrar": lookup.registrar,
                "creation_date": lookup.creation_date.strftime("%Y-%m-%d %H:%M:%S") if type(lookup.creation_date) == datetime else lookup.creation_date[0].strftime("%Y-%m-%d %H:%M:%S"),
                "expiration_date": lookup.expiration_date.strftime("%Y-%m-%d %H:%M:%S") if type(lookup.expiration_date) == datetime else lookup.expiration_date[0].strftime("%Y-%m-%d %H:%M:%S"),
                "updated_date" : lookup.updated_date.strftime("%Y-%m-%d %H:%M:%S") if type(lookup.updated_date) == datetime else lookup.updated_date[0].strftime("%Y-%m-%d %H:%M:%S"),
                "name_servers": lookup.name_servers

            },
            "registrant": {
                "name": lookup.name,
                "organization": lookup.org,
                "email": lookup.emails,
                "country": lookup.country,
                "state": lookup.state,
                "city": lookup.city,
            },
        }

    def init_values(self):
        self.domain_host_check()


    def run(self):
        if "." not in self.host or not self.is_valid():
            return {"error" : "IP/Domain appears to be offline or invalid?"}
        self.init_values()
        print()
        info("Looking up IP...")
        self.ip_lookup()
        success("Completed IP lookup!")

        print()

        info("Scanning public VPN records...")
        response = vpn(self.report["basic"]["ip"])
        if response:
            self.report["vpn_check"] = response
        success("Scanned public vpn records!")

        print()

        info("Searching whois records...")
        self.whois_()
        success("Whois records recovered!")

        print()

        info("Scanning port...")
        scan(self.report["basic"]["ip"], self.report)
        success("Port scan finished!")

        print()

        if self.report.get("ports"):
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