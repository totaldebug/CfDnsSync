from cfdnssync.config import Config
from cfdnssync.factory import factory, logger
from cfdnssync.util.get_ip import get_public_ip
from cfdnssync.zones import CfZone, CfRecord

class SyncConfig:
    def __init__(self, config: Config):
        try:
            self.zones=list(config["zones"])
        except Exception:
            logger.error(f"sync section missing from config, add this to the config file: {config.config_yml}")

    def __getitem__(self, key):
        return self.zones[key]

    def __contains__(self, key):
        return key in self.zones


class Sync:
    def __init__(self, config: Config, progressbar=None):
        self.config = config
        self.sync_config = SyncConfig(config)
        self.cf = factory.cloudflare_api()
        self.ip_addresses = {4: None, 6: None}
        self._progressbar = progressbar

    def progressbar(self, iterable, **kwargs):
        if self._progressbar:
            pb = self._progressbar(iterable, **kwargs)
            with pb as records:
                yield from records
        else:
            yield from iterable

    def sync(self, dry_run=False):
        zones = factory.zones(enabled_only=True)


        # Loop through enabled zones.
        for zone in zones:
            logger.info(f"Getting zone: {zone.zone_id}")
            # grab the zone identifier
            try:
                cf_zones: list[CfZone] = factory.cf_zones(cf=self.cf, zone_id=zone.zone_id)

            except Exception as e:
                logger.error(f'Unable to get zone: {zone.zone_id} from CloudFlare: {e}')
                continue

            # there should only be one zone
            for cf_zone in sorted(cf_zones, key=lambda v: v.id):
                logger.info(f"Processing Zone: {cf_zone.id} with name: {cf_zone.name}")

            it = self.progressbar(zone.subdomains, desc="Processing subdomains")
            for dns_record in it:
                if self.ip_addresses[4] and dns_record.type != 'AAAA':
                    public_ip = self.ip_addresses[4]
                elif self.ip_addresses[6] and dns_record.type == 'AAAA':
                    public_ip = self.ip_addresses[6]
                else:
                    public_ip_ver = get_public_ip(self.config, dns_record.type)
                    self.ip_addresses[public_ip_ver[0]] = public_ip_ver[1]
                    public_ip = public_ip_ver[1]

                if dns_record.name == "@":
                    name = cf_zone.name
                else:
                    name = f"{dns_record.name}.{cf_zone.name}"
                matched_record = None
                for cf_dns_record in cf_zone.records:
                    if name == cf_dns_record.name and dns_record.type == cf_dns_record.type:
                        matched_record = cf_dns_record
                        continue
                if matched_record:
                    if dns_record.state == "absent":
                        # Remove DNS record from CloudFlare
                        self.cf.delete_record(matched_record, dry_run=dry_run)
                    elif dns_record.state == "present":
                        # Update the record on CloudFlare
                        self.cf.update_record(dns_record, matched_record, public_ip, dry_run=dry_run)
                elif dns_record.state == "present":
                    # Add the record to CloudFlare
                    self.cf.add_record(dns_record, cf_zone.id, cf_zone.name, public_ip, dry_run=dry_run)
                elif dns_record.state == "absent":
                    # Record doesnt exist and is state absent, no action required.
                    logger.info(f"[SKIP] {name} already absent.")
