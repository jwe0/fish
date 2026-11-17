import tls_client, re, datetime

def proton_lookup(email):
    report = {}
    session = tls_client.Session()
    api = "https://api.protonmail.ch/pks/lookup?op=index&search={}".format(email)


    response = session.get(api)

    if "info:1:1" in response.text:
        patterns = [
            ("2048:(.*)::", "RSA 2048"), 
            ("4096:(.*)::", "RSA 4096"), 
            ("22::(.*)::", "X25519")
        ]

        for pattern, method in patterns:
            try:
                timestamp = int(re.search(pattern, response.text).group(1))
                created = datetime.datetime.fromtimestamp(timestamp)
                report = {
                    "created" : created,
                    "method" : method,
                    "pub_key" : "https://api.protonmail.ch/pks/lookup?op=get&search={}".format(email)
                }
            except:
                pass

    if not report:
        report = {"error" : "API FAIL"}
    return report




