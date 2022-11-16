from cfdnssync.decorators.measure_time import measure_time
from cfdnssync.factory import factory, logger
from cfdnssync.version import version


def sync(zones: list[str], dry_run: bool, no_progress_bar: bool):
    """
    Perform sync to cloudflare DNS
    """

    logger.info(f"CfDnsSync [{version()}]")

    config = factory.run_config().update(
        dry_run=dry_run, progressbar=not no_progress_bar
    )


    with measure_time("Completed Sync"):
        runner = factory.sync()
        if dry_run:
            logger.info("Enabled dry-run mode: not making changes")

        runner.sync(dry_run=config.dry_run)
