import os
import time
import hashlib
import yaml
import requests
from zencore.utils.system import get_main_ipaddress


def get_update_code(hostname, ip, timestamp, key):
    hostname = hostname.upper()
    text = "hostname={}&ip={}&timestamp={}&key={}".format(hostname, ip, timestamp, key)
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def get_query_code(hostname, timestamp, key):
    hostname = hostname.upper()
    text = "hostname={}&timestamp={}&key={}".format(hostname, timestamp, key)
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def client_update(server, hostname, key, use_local_ip=False):
    timestamp = int(time.time())
    ip = use_local_ip and get_main_ipaddress() or ""
    params = {
        "hostname": hostname,
        "ip": ip,
        "timestamp": timestamp,
        "code": get_update_code(hostname, ip, timestamp, key),
    }
    response = requests.get(server, params=params)
    if response.status_code == 200:
        return True
    return False


def client_query(server, hostname, key):
    timestamp = int(time.time())
    params = {
        "hostname": hostname,
        "timestamp": timestamp,
        "code": get_query_code(hostname, timestamp, key),
    }
    response = requests.get(server, params=params)
    if response.status_code == 200:
        return response.text
    return "ERROR"


def load_config(path):
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as fobj:
        return yaml.load(fobj)


def save_config(settings, path):
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fobj:
        yaml.dump(settings, fobj)


def input_config():
    hostname = ""
    server = ""
    update_key = ""
    use_local_ip = ""

    while not hostname:
        hostname = input("Hostname: ").upper()
    while not server:
        server = input("Server: ")
    while not update_key:
        update_key = input("Update key: ")
    while not use_local_ip in ("y", "n"):
        use_local_ip = input("Use local ip (y/n): ").lower()
    if use_local_ip == "y":
        use_local_ip = True
    else:
        use_local_ip = False

    return {
        hostname: {
            "server": server,
            "key": update_key,
            "use-local-ip": use_local_ip,
        }
    }

