from functools import wraps
import click


def command():
    """
    Wrapper to lazy load commands when commands being executed only
    """

    def decorator(fn):
        @click.command()
        @wraps(fn)
        def wrap(*args, **kwargs):
            import importlib

            name = fn.__name__
            module = importlib.import_module(f".commands.{name}", package=__package__)
            cmd = getattr(module, name)

            try:
                cmd(*args, **kwargs)
            except RuntimeError as e:
                from click import ClickException

                raise ClickException(f"Error running {name} command: {str(e)}")

        return wrap

    return decorator

@click.group(invoke_without_command=True)
@click.option("--version", is_flag=True, help="Print version and exit")
@click.pass_context
def cli(ctx, version: bool):
    """
    CfDnsSync updates Cloudflare DNS records with local public IP
    """

    if version:
        from .version import version
        print(f"CfDnsSync {version()}")
        return

    if not ctx.invoked_subcommand:
        sync()


@command()
def info():
    """
    Print application and environment version info
    """

    pass

@command()
@click.option(
    "--zone",
    "-z",
    "zone_ids",
    multiple=True,
    show_default=True,
    help="Show specific zone only, can be used multiple times.",
)
@click.option(
    "--enabled-only",
    "enabled_only",
    is_flag=True,
    show_default=True,
    help="Only show enabled zones",
)
@click.option(
    "--show-subdomains",
    "show_subdomains",
    is_flag=True,
    show_default=True,
    help="Show a list of subdomains",
)
def zones():
    """
    Print configured zones
    """
    pass


@command()
@click.option(
    "--zones",
    "zones",
    type=str,
    multiple=True,
    show_default=True,
    help="Sync specific zone only",
)
@click.option(
    "--dry-run",
    "dry_run",
    type=bool,
    default=False,
    is_flag=True,
    help="Dry run: Do not make changes",
)
@click.option(
    "--no-progress-bar",
    "no_progress_bar",
    type=bool,
    default=False,
    is_flag=True,
    help="Don't output progress bars",
)
def sync():
    """
    Perform sync with Cloudflare DNS
    """
    pass

@command()
def bug_report():
    """
    Create a pre-populated GitHub issue with information about your configuration
    """
    pass

@command()
@click.option(
    "--pr",
    type=int,
    default=False,
    help="Install cfdnssync for specific Pull Request",
)
def update():
    """
    Update CfDnsSync to the latest version using pipx
    \b
    $ cfdnssync update
    Updating CfDnsSync to latest using pipx
    upgraded package cfdnssync from 1.0.0 to 2.0.0 (location: /.local/pipx/venvs/cfdnssync)
    """
    pass


cli.add_command(info)
cli.add_command(zones)
cli.add_command(sync)
cli.add_command(bug_report)
cli.add_command(update)
