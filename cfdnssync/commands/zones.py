from cfdnssync.factory import logger
from cfdnssync.version import version as get_version

def zones(print=logger.info):
    
    print(f"CfDnsSync Version: {get_version()}")
