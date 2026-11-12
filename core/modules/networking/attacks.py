from ftplib import FTP

def ftp_attack(ip):
    ftp = FTP(ip)   
    response = ftp.login()
    if "230" and "logged in" in response:
        return response
    return "Anonymous login blocked"