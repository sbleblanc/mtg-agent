import re
import json
import itertools as it
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



@cli.command()
@click.argument('input_rules', type=click.Path(exists=True, path_type=Path))
@click.argument('output_md', type=click.Path(path_type=Path))
def convert_rules_to_md(input_rules: Path, output_md: Path):

    h2_regex = re.compile(r'^\d\. ')
    h3_regex = re.compile(r'^\d{3}\. ')
    nested_regex = re.compile(r'^\d{3}\.\d[a-z] ')

    markdown_content = ["# Magic: The Gathering Comprehensive Rules"]

    with input_rules.open() as f:
        content_iter = it.dropwhile(lambda l: l.strip() != "Credits", f)
        next(content_iter) # Ignore intro and ToC
        next(content_iter) # Ignore the "Credits" Line

        for line in (
                l.strip()
                for l in it.filterfalse(lambda l: len(l.strip()) == 0, content_iter)
        ):
            if line == "Glossary":
                break
            if h2_regex.match(line):
                markdown_content.append(f"## {line}")
            elif h3_regex.match(line):
                markdown_content.append(f"### {line}")
            elif nested_regex.match(line):
                markdown_content.append(f"  - {line}")
            else:
                markdown_content.append(f"- {line}")

    with output_md.open(mode="w") as f:
        f.write("\n".join(markdown_content))


if __name__ == '__main__':
    cli()