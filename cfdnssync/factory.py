import CloudFlare

from cfdnssync.zones import CfRecord, CfZone

class Factory:
    def sync(self):
        from cfdnssync.sync import Sync

        config = self.config()

        return Sync(config)

    def progressbar(self, enabled=True):
        if enabled:
            import warnings
            from functools import partial

            from tqdm import TqdmExperimentalWarning
            from tqdm.rich import tqdm

            from cfdnssync.console import console

            warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)

            return partial(tqdm, options={'console': console})

        return None

    def run_config(self):
        from cfdnssync.config import RunConfig

        config = RunConfig()

        return config


    def logging(self):
        import logging

        from cfdnssync.logging import initialize

        config = self.config()
        initialize(config)

        return logging

    def logger(self):
        logger = self.logging().getLogger("CfDnsSync")
        config = self.config()

        from cfdnssync.logger.filter import LoggerFilter
        logger.addFilter(LoggerFilter(config["logging"]["filter"], logger))

        return logger

    def console_logger(self):
        from rich.logging import RichHandler

        from cfdnssync.console import console
        from cfdnssync.rich_addons import RichHighlighter

        config = self.config()
        return RichHandler(console=console, show_time=config.log_console_time, log_time_format='[%Y-%m-%d %X]', show_path=False, highlighter=RichHighlighter(),)

    def config(self):
        from cfdnssync.config import Config

        return Config()

    def zones(self, zone_ids:list[str] = None, enabled_only:bool=None):
        from cfdnssync.zones import Zone
        config = self.config()
        zones = [Zone(zone) for zone in config.zones]
        filtered_zones = []
        if enabled_only:
            filtered_zones.extend(zone for zone in zones if zone.enabled is True)
        if zone_ids:
            for zone in filtered_zones:
                if zone.zone_id not in zone_ids:
                    filtered_zones.remove(zone)
        if not zone_ids and not enabled_only:
            filtered_zones = zones
        return filtered_zones

    def cloudflare_api(self):
        from cfdnssync.cloudflare_api import CloudflareApi
        return CloudflareApi(factory)

    def cf_zones(self, cf: CloudFlare, zone_id):
        zones: CfZone = [CfZone(zone) for zone in cf.get_zone(zone_id)]
        for zone in zones:
            zone.records = [CfRecord(record) for record in cf.get_dns_records(zone.id)]
        return zones

factory = Factory()
logger = factory.logger()
logging = factory.logging()
