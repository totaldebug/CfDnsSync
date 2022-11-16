from dataclasses import dataclass
from os import getenv
from os.path import exists

from cfdnssync.path import config_yml, default_config_file
from cfdnssync.factory import factory
from cfdnssync.zones import Zone

@dataclass
class RunConfig:
    """
    Class to hold runtime config parameters
    """

    dry_run: bool = False
    batch_delay: int = 5
    progressbar: bool = True

    def update(self, **kwargs):
        for name, value in kwargs.items():
            self.__setattr__(name, value)

        return self


class ConfigLoader:
    @staticmethod
    def load(path: str):
        if path.endswith('.yml'):
            return ConfigLoader.load_yaml(path)
        raise RuntimeError(f'Unknown file type: {path}')

    @staticmethod
    def write(path: str, config):
        if path.endswith('.yml'):
            return ConfigLoader.write_yaml(path, config)
        raise RuntimeError(f'Unknown file type: {path}')

    @staticmethod
    def copy(src: str, dst: str):
        import shutil

        shutil.copyfile(src, dst)

    @staticmethod
    def rename(src: str, dst: str):
        from os import rename

        rename(src, dst)

    @staticmethod
    def load_yaml(path: str):
        import yaml

        with open(path, "r", encoding="utf-8") as fp:
            try:
                config = yaml.safe_load(fp)
            except yaml.YAMLError as e:
                raise RuntimeError(f"Unable to parse {path}: {e}") from e
        return config

    @staticmethod
    def write_yaml(path: str, config):
        import yaml

        with open(path, "w", encoding="utf-8") as fp:
            yaml.dump(config, fp, allow_unicode=True, indent=2)


class Config(dict):
    initialized = False
    config_yml = config_yml

    def __getitem__(self, item):
        if not self.initialized:
            self.initialize()
        return dict.__getitem__(self, item)

    def __contains__(self, item):
        if not self.initialized:
            self.initialize()
        return dict.__contains__(self, item)



    @property
    def log_file(self):
        from os.path import join

        from .path import log_dir

        return join(log_dir, self["logging"]["filename"])

    @property
    def log_debug(self):
        return ("log_debug_messages" in self and self["log_debug_messages"]) or self["logging"]["debug"]

    @property
    def log_append(self):
        return self["logging"]["append"]

    @property
    def log_console_time(self):
        return self["logging"]["console_time"]

    @property
    def ip_method(self) -> str:
        return self["ip"]["method"]

    @property
    def zones(self):
        return self['zones']

    def initialize(self):
        """
        Config load order:
        - load config.yml
        - if config.yml is missing, error
        """
        self.initialized = True

        loader = ConfigLoader()
        defaults = loader.load(default_config_file)
        self.update(defaults)

        if not exists(self.config_yml):
            loader.copy(default_config_file, self.config_yml)

        config = loader.load(self.config_yml)
        self.merge(config, self)

    # https://stackoverflow.com/a/20666342/2314626
    def merge(self, source, destination):
        for key, value in source.items():
            if isinstance(value, dict):
                # get node or create one
                node = destination.setdefault(key, {})
                self.merge(value, node)
            else:
                destination[key] = value

        return destination
