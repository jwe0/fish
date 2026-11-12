import json, threading,  tls_client
from core.modules.logging import *
from core.modules.social_media.extra_attacks.github import github

class Online:
    def __init__(self, username):
        self.username = username
        self.hits = {}
        self.errors = {}
        self.link_file = "core/dependencies/sites.json"
        self.links = json.load(open(self.link_file))
        self.link_count = len(self.links)
        self.completed = 0
        self.session = tls_client.Session()

        self.extra_info = {
            "GitHub" : github
        }

    def check_site(self, url, type, code, site):
        try:
            headers = {
                "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding" : "gzip, deflate, br, zstd",
                "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:158.0) Gecko/20100101 Firefox/158.0"
            }
            response = self.session.get(
                url.format(self.username, headers=headers)
            )

            match type:
                case "status":
                    if response.status_code == 200:
                        self.hits[site] = {
                            "site" : site,
                            "url" : url.format(self.username),
                            "check_type" : type,
                            "expected" : code,
                            "recieved" : response.status_code
                        }
                case "title":
                    ""
                case "content":
                    ""

        except Exception as e:
            self.errors[site] = {
                "error" : e
            }
        self.completed += 1

    def username_lookup(self):
        info("Searching for username on {} sites".format(self.link_count))
        for site in self.links:
            site_info = self.links[site]

            link = site_info["link"]
            type = site_info["type"]
            code = site_info["code"]

            threading.Thread(
                target=self.check_site,
                args=[
                    link, 
                    type,
                    code,
                    site
                ]
            ).start()

        while self.completed < self.link_count:
            message = info(f"Scanned [{self.completed}/{self.link_count}] [{len(self.hits)} hits] [{len(self.errors)} errors]", False)
            print(message, end="\r")
        return self.hits

    def run(self):
        hits = self.username_lookup()

        for hit in hits:
            info = hits[hit]
            if hit in self.extra_info:
                extra = self.extra_info[info["site"]](info["url"], self.session)

                self.hits[hit]["extra"] = extra

        return self.hits