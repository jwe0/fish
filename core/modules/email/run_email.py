import socket, json
from core.modules.general import flatten_results
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

        


    def run(self):
        self.host_lookup()
        user_lookup = self.online.run()
        self.report["username"] = user_lookup
        return self.report