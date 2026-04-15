import re
import json
import itertools as it
from pathlib import Path

from mtg_agent.agents.synthetic import get_synthetic_question_generator_agent, SyntheticRuleQuestion

import click
import pandas as pd
import numpy as np
from tqdm import tqdm
from transformers import AutoTokenizer
from langchain_text_splitters import MarkdownHeaderTextSplitter
from sentence_transformers import SentenceTransformer



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
            "id": i,
            "h1": chunk.metadata.get("h1", ""),
            "h2": chunk.metadata.get("h2", ""),
            "h3": chunk.metadata.get("h3", ""),
            "h4": chunk.metadata.get("h4", ""),
            "content": chunk.page_content
        }
        for i, chunk in enumerate(rules_splits)
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


@cli.command()
@click.option("-n", "--num-questions", type=int, default=5)
@click.argument('chunks_json', type=click.Path(path_type=Path))
@click.argument('chunks_with_questions_json', type=click.Path(path_type=Path))
def generate_synthetic_rule_questions(num_questions:int, chunks_json: Path, chunks_with_questions_json: Path):
    # import logfire
    #
    # logfire.configure(send_to_logfire='if-token-present')
    # logfire.instrument_pydantic_ai()

    agent = get_synthetic_question_generator_agent(num_questions=num_questions)

    with chunks_json.open(mode="r") as f:
        chunks = json.load(f)

    chunks_with_questions = []

    for chunk in tqdm(chunks):
        prompt = f"## {chunk['h2']}\n### {chunk['h3']}\n{chunk['content']}"
        # Need to find a better way to handle the model not answering in the right format
        try:
            res = agent.run_sync(prompt)
        except Exception as e:
            continue
        # print(res.output)
        chunks_with_questions.append({
            "id": chunk["id"],
            "content": prompt,
            "questions": [
                syn_rule.model_dump()
                for syn_rule in res.output
            ]
        })

    with chunks_with_questions_json.open(mode="w") as f:
        json.dump(chunks_with_questions, f, indent=2)


@cli.command()
@click.option("--seed", type=int, default=42)
@click.option("--test-ratio", type=float, default=0.2)
@click.option("--granularity", type=click.Choice(["chunk", "question"]))
@click.argument('chunks_with_questions_json', type=click.Path(dir_okay=False, path_type=Path))
@click.argument('output_dir', type=click.Path(file_okay=False, path_type=Path))
@click.argument('output_prefix', type=str)
def build_rule_retrieval_ds(
        seed: int,
        test_ratio: float,
        granularity: str,
        chunks_with_questions_json: Path,
        output_dir: Path,
        output_prefix: Path
):

    with chunks_with_questions_json.open(mode="r") as f:
        chunks = json.load(f)

    chunks_df = pd.DataFrame(chunks)

    qid_counter = it.count()
    chunks_df['questions'] = chunks_df['questions'].apply(lambda qs: [{**q, "question_id": next(qid_counter)} for q in qs])
    chunks_df.rename(columns={"id": "chunk_id"}, inplace=True)

    def explode(df):
        df = df.explode("questions")
        df[['rule_number', 'question', 'question_id']] = df['questions'].apply(lambda x: pd.Series(x))
        return df.drop('questions', axis=1)

    if granularity == "chunk":
        chunks_df = chunks_df.sample(frac=1.0, random_state=seed)
        take = int(test_ratio * chunks_df.shape[0])
        test_df = explode(chunks_df.iloc[:take])
        train_df = explode(chunks_df.iloc[take:])
    else:
        questions_df = explode(chunks_df).sample(frac=1.0, random_state=seed)
        take = int(test_ratio * questions_df.shape[0])
        test_df = questions_df.iloc[:take]
        train_df = questions_df.iloc[take:]

    train_df.to_csv(output_dir / f"{output_prefix}_{granularity}_train.csv", index=False)
    test_df.to_csv(output_dir / f"{output_prefix}_{granularity}_test.csv", index=False)


@cli.command()
@click.option("-m", "--model-name", type=str, default="Qwen/Qwen3-Embedding-0.6B")
@click.option("-d", "--device", type=str, default="cuda:0")
@click.option("-b", "--batch-size", type=int, default=4)
@click.option("-s", "--suffix", type=str, default="qwen3_emb_600m")
@click.argument('dataset_path', type=click.Path(dir_okay=False, path_type=Path))
def generate_vectors(
        model_name: str,
        device: str,
        batch_size: int,
        suffix: str,
        dataset_path: Path,
):
    df = pd.read_csv(dataset_path)

    model = SentenceTransformer(model_name, device=device)
    doc_embeddings = model.encode(
        df['content'].to_list(),
        batch_size=batch_size,
        show_progress_bar=True,
        device=device
    )

    np.savez(
        dataset_path.with_stem(f"{dataset_path.stem}_{suffix}").with_suffix(".npz"),
        embeddings=doc_embeddings,
        allow_pickle=False
    )


if __name__ == '__main__':
    cli()