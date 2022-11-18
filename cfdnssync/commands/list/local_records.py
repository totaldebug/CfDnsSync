from typing import Optional
from rich.table import Table

from cfdnssync.console import print
from cfdnssync.factory import factory
from cfdnssync.zones import Zone, Record

def local_records(zone_names: Optional[str] = None):
    """Gets all Zones DNS Records
    """
    cf = factory.cloudflare_api()
    zones = cf.get_zone(name=zone_names)
    if zones:
        zones = [Zone(zone) for zone in zones]

        for zone in zones:
            zone.records = [Record(record) for record in cf.get_dns_records(zone.id)]

        table = Table(
            show_header=True, header_style="bold dark_orange3", title="CloudFlare Domain Records"
        )
        table.add_column("Id", style="dim", width=6)
        table.add_column("Record")
        table.add_column("Type")
        table.add_column("Content")
        table.add_column("TTL")
        table.add_column("Proxied")
        for zone in zones:
            if zone.records:
                for record in zone.records:
                    if record.type in ['A', 'AAAA']:
                        name = f"[link=https://{record.name}]{record.name}[/]"
                    else:
                        name = record.name
                    table.add_row(record.id, name, record.type, record.content, str(record.ttl), str(record.proxied))
        print(table)
