import socket, whois
from core.modules.logging import error
from datetime import datetime
from core.modules.social_media.run_social_media import Online

class Email:
    def __init__(self, email):
        self.email   = email
        self.report  = {}

        self.username = self.email.split("@")[0]
        self.host     = self.email.split("@")[1]

        self.report["basic"] = {
            "username" : self.username,
            "host" : self.host
        }

        self.online = Online(self.username)

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
  


    def run(self):
        self.host_lookup()
        self.whois_()
        user_lookup = self.online.run()
        if user_lookup:
            self.report["username"] = user_lookup
        return self.report