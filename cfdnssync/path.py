from os import getenv, makedirs
from os.path import abspath, dirname, exists, join

class Path:
    def __init__(self):
        self.app_name = "CfDnsSync"
        self.module_path = dirname(abspath(__file__))
        self.app_path = dirname(self.module_path)

        self.ensure_dir(self.config_dir())
        self.ensure_dir(self.log_dir())

        self.default_config_file = join(self.module_path, "config.default.yml")
        self.config_yml = join(self.config_dir(), "config.yml")


    def config_dir(self):
        d = self.app_dir().user_config_dir if self.installed else self.app_path
        return getenv("CDS_CONFIG_DIR", d)


    def log_dir(self):
        d = self.app_dir().user_log_dir if self.installed else self.app_path
        return getenv("CDS_LOG_DIR", d)

    def app_dir(self):
        from appdirs import AppDirs

        return AppDirs(self.app_name)

    def installed(self):
        from cfdnssync.util.packaging import installed

        return installed()

    @staticmethod
    def ensure_dir(directory):
        if not exists(directory):
            makedirs(directory)


p = Path()

config_dir = p.config_dir()
log_dir = p.log_dir()
default_config_file = p.default_config_file
config_yml = p.config_yml
