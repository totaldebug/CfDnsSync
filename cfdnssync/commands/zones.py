from cfdnssync.factory import factory, logger
from cfdnssync.version import version as get_version

def zones(zone_ids: list[str] = None, enabled_only: bool = False, show_records: bool = False,print=logger.info):

    print(f"CfDnsSync Version: {get_version()}")

    if zones := factory.zones(zone_ids=zone_ids, enabled_only=enabled_only):
        if enabled_only:
            print("Enabled Zones Only")
        elif zone_ids:
            print(f"Showing Zones {zone_ids}")
        print("==================")
        print(f"Zone Count: {len(zones)}")
        records = sum(len(zone.records) for zone in zones)
        print(f"Sub-Domains: {records}")
        if show_records:
            print("==================")
            for zone in zones:
                subs = [sub.name for sub in zone.records]
                print(f"{zone.zone_id}: {','.join(subs)}")

    else:
        print("There are no zones matching this criteria")
