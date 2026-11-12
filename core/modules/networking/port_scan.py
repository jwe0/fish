import socket, time
from core.modules.logging import error

def check_banner(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((ip, int(port)))

        banner = s.recv(1024).decode().strip()
        s.close()
        return banner
    except:
        return None

def scan(ip, report):
    result = {}
    ports = {
        "80"  : "HTTP",
        "443" : "HTTPS",
        "22"  : "SSH",
        "21"  : "FTP"
    }

    for port in ports:
        service = ports[port]
        try:
            start = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            con = s.connect_ex((ip, int(port)))
            if con == 0:
                end = time.time()

                taken = end - start
                if con == 0:
                    result[port] = {
                        "service" : service,
                        "ports"   : port,
                        "combo"   : f"{ip}:{port}",
                        "taken"   : f"{taken}s"
                    }
                    banner = check_banner(ip, port)
                    if banner:
                        result[port]["banner"] = banner
        except Exception as e:
            error(e)
    report["ports"] = result