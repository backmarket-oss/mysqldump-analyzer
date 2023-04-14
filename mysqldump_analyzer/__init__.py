from typing import Any

import click
import yaml

from mysqldump_analyzer.diff import diff_dumps


@click.group()
def main() -> None:
    """Main entry point."""
    pass


@main.command()
@click.argument("dumps", nargs=-1, type=click.File())
def diff(dumps: Any) -> None:
    result = diff_dumps(**{dump.name: dump for dump in dumps})
    if result:
        print(result)
