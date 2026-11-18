import socket, whois
from core.modules.logging import error
from datetime import datetime
from core.modules.social_media.run_social_media import Online
from core.modules.email.lookups.proton import proton_lookup

class Email:
    def __init__(self, email):
        self.email   = email[0]
        self.report  = {}

        self.extra_attacks = {
            "proton" : {
                "func" : proton_lookup,
                "type" : "Proton API",
                "hosts" : ["proton.me", "proton.com"] 
            }
        }

    def host_lookup(self):
        try:
            info = socket.gethostbyname_ex(self.host)
            hostname = info[0]
            aliases  = info[1]
            addreses = info [2]

            self.report["host"] = {
                "hostname" : hostname,
                "aliases" : aliases,
                "addreses" : addreses 
            }

        except Exception as e:
            return {"message" : e}

    def whois_(self):
        lookup = whois.whois(self.host)

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
        self.username = self.email.split("@")[0]
        self.host     = self.email.split("@")[1]

        self.report["basic"] = {
            "username" : self.username,
            "host" : self.host
        }
        self.online = Online([self.username])

    def extra_domain_scan(self):
        for extra in self.extra_attacks:
            information = self.extra_attacks[extra]

            func = information["func"]
            hosts = information["hosts"]
            type = information["type"]

            if self.host in hosts:
                self.report["lookups"] = {}
                response = func(self.email)
                self.report["lookups"][type] = response


    def run(self):
        if "@" not in self.email or "." not in self.email:
            return {"error" : "Please provide a valid email format"}
        self.init_values()
        self.host_lookup()
        self.whois_()
        self.extra_domain_scan()
        user_lookup = self.online.run()
        if user_lookup:
            self.report["username"] = user_lookup
        return self.report