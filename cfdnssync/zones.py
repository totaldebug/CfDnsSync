from dataclasses import dataclass


class Zone:
    """
    Class containing zone items
    """
    def __init__(self, zone):
        self.zone = zone

    @property
    def zone_id(self):
        return self.zone['zone']

    @property
    def api_token(self):
        return self.zone['api_token']

    @property
    def enabled(self):
        return self.zone['enabled']

    @property
    def subdomains(self):
        return [SubDomain(subdomain) for subdomain in self.zone['records']]

class SubDomain:
    """
    Class containing subdomains for a zone
    """

    def __init__(self, subdomain):
        self.sub = subdomain

    @property
    def name(self):
        return self.sub['name']

    @property
    def type(self):
        return self.sub['type']

    @property
    def ttl(self):
        try:
            ttl = int(self.sub["ttl"])
        except:
            ttl = 300  # default Cloudflare TTL
            print(
                "No config detected for 'ttl' - defaulting to 300 seconds (5 minutes)")
        if self.proxied:
            ttl = 1
        elif ttl < 30:
            ttl = 30  #
            print("TTL is too low - defaulting to 30 seconds")
        return ttl

    @property
    def proxied(self):
        return self.sub['proxied']

    @property
    def state(self):
        return self.sub['state']


@dataclass
class CfRecord:
    def __init__(self, record):
        self.rec = record

    @property
    def id(self):
        return self.rec["id"]

    @property
    def zone_id(self):
        return self.rec["zone_id"]

    @property
    def name(self):
        return self.rec["name"]

    @property
    def type(self):
        return self.rec["type"]

    @property
    def content(self) -> str:
        return self.rec["content"]

    @property
    def proxiable(self) -> bool:
        return self.rec["proxiable"]

    @property
    def proxied(self) -> bool:
        return self.rec["proxied"]

    @property
    def ttl(self) -> int:
        return self.rec["ttl"]

    @property
    def locked(self) -> bool:
        return self.rec["locked"]

    @property
    def meta(self) -> dict:
        return self.rec["meta"]

    @property
    def created_on(self):
        return self.rec["created_on"]

    @property
    def modified_on(self):
        return self.rec["modified_on"]

@dataclass
class CfZone:

    def __init__(self, zone):
        self.zone = zone

    @property
    def id(self):
        return self.zone["id"]

    @property
    def name(self):
        return self.zone["name"]

    @property
    def status(self):
        return self.zone["active"]

    @property
    def paused(self) -> bool:
        return self.zone["paused"]

    @property
    def type(self) -> str:
        return self.zone["type"]

    @property
    def development_mode(self) -> int:
        return self.zone["development_mode"]

    @property
    def name_servers(self) -> list:
        return self.zone["name_servers"]

    @property
    def original_name_servers(self) -> list:
        return self.zone["original_name_servers"]

    @property
    def original_registrar(self) -> str:
        return self.zone["original_registrar"]

    @property
    def original_dnshost(self) -> str | None:
        return self.zone["original_dnshost"]

    @property
    def records(self) -> list[CfRecord] | None:
        return self._records

    @records.setter
    def records(self, records: list[CfRecord]):
        self._records = records


    @property
    def modified_on(self):
        return self.zone["modified_on"]

    @property
    def created_on(self):
        return self.zone["created_on"]

    @property
    def activated_on(self):
        return self.zone["activated_on"]
