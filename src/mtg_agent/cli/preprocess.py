import re
import json
import itertools as it
from pathlib import Path

import click
import numpy as np
from transformers import AutoTokenizer
from langchain_text_splitters import MarkdownHeaderTextSplitter


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
    h4_regex = re.compile(r'^\d{3}\.\d+\. ')

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
            elif h4_regex.match(line):
                markdown_content.append(f"#### {line}")
            else:
                markdown_content.append(f"- {line}")

    with output_md.open(mode="w") as f:
        f.write("\n".join(markdown_content))


@cli.command()
@click.option("-e", "--embedding-model", default="google/gemma-4-E4B")
@click.argument('input_rules_md', type=click.Path(exists=True, path_type=Path))
@click.argument('chunks_json', type=click.Path(path_type=Path))
def chunk_rules(
        embedding_model: str,
        input_rules_md: Path,
        chunks_json: Path
):
    tok = AutoTokenizer.from_pretrained(embedding_model)

    with input_rules_md.open(mode="r") as f:
        markdown_rules = f.read()

    headers_to_split_on = [
        ("#", "h1"),
        ("##", "h2"),
        ("###", "h3"),
        ("####", "h4"),
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers=False)
    rules_splits = markdown_splitter.split_text(markdown_rules)

    chunks = [
        {
            "h1": chunk.metadata.get("h1", ""),
            "h2": chunk.metadata.get("h2", ""),
            "h3": chunk.metadata.get("h3", ""),
            "h4": chunk.metadata.get("h4", ""),
            "content": chunk.page_content
        }
        for chunk in rules_splits
    ]

    token_counts = np.array([
        len(tok.tokenize(
            f"{chunk['h2']}\n{chunk['h3']}\n{chunk['h4']}\n{chunk['content']}"
        ))
        for chunk in chunks
    ])

    print(np.quantile(token_counts, 0.))
    print(np.quantile(token_counts, 0.25))
    print(np.quantile(token_counts, 0.5))
    print(np.quantile(token_counts, 0.75))
    print(np.quantile(token_counts, 1.0))

    with chunks_json.open(mode="w") as f:
        json.dump(chunks, f, indent=2)


if __name__ == '__main__':
    cli()