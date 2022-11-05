import sys

from cfdnssync.factory import factory, logger
from cfdnssync.path import config_dir, log_dir
from cfdnssync.version import version as get_version


def info(print=logger.info):
#def info():
    print(f"CfDnsSync Version: {get_version()}")

    py_version = sys.version.replace("\n", "")
    print(f"Python Version: {py_version}")
    print(f"Config Dir: {config_dir}")
    print(f"Log Dir: {log_dir}")

    config = factory.config()
    print(f"Log File: {config.log_file}")
    print(f"Config File: {config.config_yml}")
