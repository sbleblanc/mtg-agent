import re
import json
from pathlib import Path

import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument('input_dump', type=click.Path(exists=True, path_type=Path))
@click.argument('output_tasks', type=click.Path(path_type=Path))
def prepare_ls_tasks(
        input_dump: Path,
        output_tasks: Path
):
    card_regex = re.compile(r'\[\[([^]]+)]]')




if __name__ == '__main__':
    cli()