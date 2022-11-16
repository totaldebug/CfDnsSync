import requests
import ipaddress
from subprocess import Popen, PIPE

from cfdnssync.config import Config

def get_public_ip(config: Config, record_type: str):
    v = 6 if record_type == "AAAA" else 4

    # Dig resolving method
    if config.ip_method == "dig":
        resolvers = {
            4: "resolver1.opendns.com",
            6: "resolver1.ipv6-sandbox.opendns.com",
        }
        p = Popen(["dig", "+short", "myip.opendns.com", record_type, f"@{resolvers[v]}", f"-{v}"], stdin=PIPE, stderr=PIPE, stdout=PIPE)

        output, err = p.communicate()
        public_ip = output.decode().rstrip()

    else:
        r = requests.get(f"https://ipv{v}.icanhazip.com")
        public_ip = r.text.rstrip()

    # Check public IP is present
    try:
        public_ip = ipaddress.ip_address(public_ip)
    except Exception as ex:
        print(f"An error occured whilst trying to get your IP Address: '{ex}'.")
        exit(1)

    return v, str(public_ip)
