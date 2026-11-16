import socket, threading
from core.modules.logging import *

class Domain:
    def __init__(self, domain):
        self.domain = domain
        self.host, self.domain_   = self.domain.split(".")
        self.report = {
            "basic"   : {
                "provided" : domain,
                "host" : self.host,
                "top_level" : self.domain_
            },
            "top_level" : {},
            "sub_domain" : {}
        }

        self.top_level_file = "core/dependencies/top_level_domains.txt"
        self.sub_domain_file = "core/dependencies/sub_domains.txt"

        self.top_levels = open(self.top_level_file).readlines()
        self.sub_domains = open(self.sub_domain_file).readlines()

        self.progress = 0

        self.total = len(self.top_levels) + len(self.sub_domains)

    def check_domain(self, domain, type_):
        try:
            response = socket.gethostbyname_ex(domain)
            hostname, aliases, addreses = response
            addreses_sorted = {}

            for address in addreses:
                addreses_sorted[address] = ""

            self.report[type_][hostname] = {
                "hostname" : hostname,
                "type" : type_,
                "aliases" : aliases,
                "addreses" : addreses_sorted
            }
        except Exception as e:
            pass
        self.progress += 1


    def check_top_levels(self):
        for top in self.top_levels:
            top = top.strip()
            top_domain = f"{self.host}.{top}"
            threading.Thread(target=self.check_domain, args=[top_domain, "top_level"]).start()

    def check_subs(self):
        for sub in self.sub_domains:
            sub = sub.strip()
            sub_domain = f"{sub}.{self.host}.{self.domain_}" 
            threading.Thread(target=self.check_domain, args=[sub_domain, "sub_domain"]).start()

    def run(self):
        info("Beggining top level domain scan thread...")
        self.check_top_levels()
        info("Beginning sub domain scan thread...")
        self.check_subs()

        while self.total != self.progress:
            pass
        print(self.report)
        input()
        return self.report