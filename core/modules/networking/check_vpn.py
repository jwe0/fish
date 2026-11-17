import json

def vpn(ip):
    vpn_file = "core/dependencies/vpn_list.json"
    vpn_list = json.load(open(vpn_file, "r"))

    for platform in vpn_list:
        
        if ip in vpn_list[platform]:
            return {
                "vpn" : "True",
                "platform" : platform,
                "ip" : ip
            }
    return None