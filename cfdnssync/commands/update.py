from typing import Optional

import click

from cfdnssync.util.execp import execp


def enable_self_update():
    from cfdnssync.util.packaging import pipx_installed, program_name

    package = pipx_installed(program_name())

    return package is not None


def has_previous_pr(pr: int):
    from cfdnssync.util.packaging import pipx_installed

    package = pipx_installed(f"cfdnssync@{pr}")

    return package is not None


def pr_number() -> Optional[int]:
    """
    Check if current executable is named cfdnssync@<pr>
    """

    import sys
    try:
        pr = sys.argv[0].split('@')[1]
    except IndexError:
        return None

    return int(pr) if pr.isnumeric() else None


def update(pr: int):
    if not pr:
        pr = pr_number()
        if pr:
            click.echo(f"Installed as pr #{pr}, enabling pr mode")

    if pr:
        if has_previous_pr(pr):
            # Uninstall because pipx doesn't update otherwise:
            # - https://github.com/pypa/pipx/issues/902
            click.echo(f"Uninstalling previous cfdnssync@{pr}")
            execp(f"pipx uninstall cfdnssync@{pr}")

        click.echo(f"Updating CfDnsSync to the pull request #{pr} version using pipx")
        execp(f"pipx install --suffix=@{pr} --force git+https://github.com/totaldebug/CfDnsSync@refs/pull/{pr}/head")
        return

    click.echo("Updating CfDnsSync to the latest version using pipx")
    execp("pipx upgrade CfDnsSync")
