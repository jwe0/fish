import tls_client, threading, json
from bs4 import BeautifulSoup
from core.modules.logging import info, error

class Fuzzer:
    def __init__(self, url):
        self.url = url[0]
        self.report = {}

        self.report["basic"] = {"url" : self.url}


        self.sub_directory_file = "core/dependencies/sub_directories.txt"
        self.sub_directorys = open(self.sub_directory_file).readlines()
        self.sub_count = len(self.sub_directorys)
        self.completed = 0
        self.session = tls_client.Session()

    def grab_title(self, content):
        soup = BeautifulSoup(content, "html.parser")
        title = soup.find("title")
        if title:
            return title.get_text().strip()
    
    def check_url(self, url, dir):
        try:
            response = self.session.get(url)
            if response.status_code != 404:
                title = self.grab_title(response.content)
                self.report[url] = {
                    "url" : url,
                    "dir" : dir,
                    "code" : response.status_code,
                    "title" : title
                }
        except:
            pass
        self.completed += 1

    def scan_directories(self):
        for dir in self.sub_directorys:
            dir = dir.strip()
            url = self.url.replace("%q", dir)
            threading.Thread(target=self.check_url, args=[url, dir]).start()



    def run(self):
        if "http" not in self.url or "https" not in self.url:
            return {"error" : "Please include https or http (https://example.com/%q)"}
        if "%q" not in self.url:
            return {"error" : "Please include the page you want to fuzz (https://example.com/%q)"}
        self.scan_directories()
        info("Fuzzer thread has been made")
        while self.completed != self.sub_count:
            message = info(f"[{self.completed}/{self.sub_count}] Completed | [{len(self.report) - 1}] hits", False)
            print(message, end="\r")
        return self.report