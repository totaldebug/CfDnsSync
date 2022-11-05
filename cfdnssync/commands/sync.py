from cfdnssync.factory import logger
from cfdnssync.version import version



def sync():
    """
    Perform sync to cloudflare DNS
    """

    logger.info(f"CfDnsSync [{version()}]")
