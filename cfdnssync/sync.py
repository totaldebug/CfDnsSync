from cfdnssync.config import Config
from cfdnssync.factory import logger

class SyncConfig:
    def __init__(self, config: Config):
        try:
            self.zones=list(config["sync"])
        except:
            logger.error(f"sync section missing from config, add this to the config file: {config.config_yml}")

    def __getitem__(self, key):
        return self.zones[key]

    def __contains__(self, key):
        return key in self.zones


class Sync:
    def __init__(self, config: Config):
        self.config = SyncConfig(config)

        for zone in self.config.zones:
            logger.info(f"Zone: { zone['zone'] }, api_token: { zone['api_token'] }")


    def sync(self, dry_run=False):
        pass
