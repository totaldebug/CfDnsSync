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
    CloudFlareUpdater updates Cloudflare DNS records with local public IP
    """

    if version:
        from .version import version
        print(f"CloudFlareUpdater {version()}")
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
cli.add_command(sync)
cli.add_command(bug_report)
cli.add_command(update)
