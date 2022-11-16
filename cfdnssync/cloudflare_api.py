import CloudFlare

from cfdnssync.zones import CfRecord, CfZone, SubDomain
from cfdnssync.factory import Factory, logging
class CloudflareApi:
    """
    Cloudflare API class abstracting common data access and dealing with requests.
    """
    def __init__(self, factory: Factory):
        self.factory = factory
        try:
            self.cf = CloudFlare.CloudFlare()
            self.logger = logging.getLogger("CfDnsSync.CloudflareApiConnection")
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            self.logger.fatal('api error: %d %s' % (e, e))

    def get_zone(self, zone_id: str = None) -> list[dict]:
        """Gets all zones from CloudFlare, or specific by zone_id

        Args:
            zone_id (str, optional): Zone ID. Defaults to None.

        Returns:
            list[dict]: List of dictionaries with zones
        """
        try:
            if zone_id:
                if (zone := self.cf.zones.get(params={'id': zone_id})):
                    return zone
                else:
                    raise
            return self.cf.zones.get()
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            self.logger.fatal('api error: %d %s' % (e, e))

    def get_dns_records(self, zone_id: str = None) -> list[dict]:
        """Get all DNS records for the associated domain

        Args:
            zone_id (str, optional): Zone ID to get. Defaults to None.

        Returns:
            list[dict]: list of zone dns records
        """
        return self.cf.zones.dns_records.get(zone_id)

    def add_record(self, local_record: SubDomain, zone_id: str, zone_name: str, public_ip: str, dry_run: bool = False) -> None:
        """Add a new DNS record to CloudFlare

        Args:
            local_record (SubDomain): local subdomain configuration
            zone_id (str): ID of the zone to place the new record
            zone_name (str): Name of the zone
            public_ip (str): Public IP Address
            dry_run (bool): is this a dry run. Defaults to False.
        """
        fqdn = f"{local_record.name}.{zone_name}"
        # no exsiting dns record to update - so create dns record
        if not dry_run:
            dns_record = {
                'name':local_record.name,
                'type':local_record.type,
                'ttl':local_record.ttl,
                'proxied':local_record.proxied,
                'content':public_ip
            }
            try:
                dns_record = self.cf.zones.dns_records.post(zone_id, data=dns_record)
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                self.logger.error(f'[ERROR] /zones.dns_records.post {fqdn} - {e} {e} - api call failed')
        self.logger.info(f'[CREATED]: {fqdn} -> {public_ip}')
        return

    def update_record(self, local_record: SubDomain, cf_record: CfRecord, public_ip: str, dry_run: bool = False) -> None:
        """Update an existing DNS Record on CloudFlare

        Args:
            local_record (SubDomain): local subdomain configuration
            cf_record (CfRecord): CloudFlare record configuration
            public_ip (str): Public IP Address
            dry_run (bool): is this a dry run. Defaults to False.
        """
        # Check if record requires updating
        if cf_record.content == public_ip and cf_record.ttl == local_record.ttl and cf_record.proxied == local_record.proxied:
            self.logger.info(f"[UPDATE] {cf_record.name} already up to date")
            return

        # If type is incorrect, dont update
        if cf_record.type != local_record.type:
            self.logger.warning(f"[NOT UPDATED] {cf_record.name}, record type conflict.")
            return

        # Update the record
        if not dry_run:
            record_update = {
                'name': cf_record.name,
                'type': cf_record.type,
                'ttl': local_record.ttl,
                'content': public_ip,
                'proxied': local_record.proxied
            }
            try:
                self.cf.zones.dns_records.put(cf_record.zone_id, cf_record.id, data=record_update)
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                self.logger.error(f'[ERROR] /zones.dns_records.put {cf_record.name} - {e} {e} - api call failed')
        self.logger.info(f'[UPDATED] {cf_record.name} {cf_record.content} -> {public_ip}')
        return

    def delete_record(self, record: CfRecord, dry_run: bool = False):
        """Delete a DNS Record from CloudFlare

        Args:
            record (CfRecord): record that should be deleted
            dry_run (bool): is this a dry run. Defaults to False.
        """
        if not dry_run:
            try:
                self.cf.zones.dns_records.delete(record.zone_id, record.id)
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                self.logger.error(f'[ERROR] /zones.dns_records.delete {record.name} - {e} {e} - api call failed')
        self.logger.info(f'[DELETED] {record.name} {record.type} {record.content}')



    def connect(self, token: str):
        """Connect to CloudFlare API

        Args:
            token (str): CloudFlare API Token

        Returns:
            CloudFlare: cloudflare instance
        """
        try:
            return CloudFlare.CloudFlare(token=token)
        except ConnectionError as e:
            self.logger.error(e)
        self.logger.error("No more methods to connect. Giving up.")
        exit(1)
