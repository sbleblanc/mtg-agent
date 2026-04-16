from collections import OrderedDict

import click
import mlflow
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from usearch.index import search, MetricKind, BatchMatches
from sklearn.metrics import ndcg_score

@click.group()
def cli():
    pass

@cli.command()
def compute_retrieval_metrics():

    ds_df = pd.read_csv("data/rules/mtg_rules_20260227_question_test.csv")
    doc_embeddings = np.load("data/rules/mtg_rules_20260227_question_test_qwen3_emb_600m.npz")['embeddings']

    device = "cuda:0"
    model_name = "Qwen/Qwen3-Embedding-0.6B"
    batch_size = 128
    query_prompt = "Instruct: Given a rule search query, retrieve relevant rule passages that answer the query\nQuery:"

    model = SentenceTransformer(model_name, device=device)
    query_embeddings = model.encode(
        ds_df['question'].to_list(),
        prompt=query_prompt,
        # normalize_embeddings=True,
        batch_size=batch_size,
        show_progress_bar=True,
        device=device
    )

    matches: BatchMatches = search(doc_embeddings, query_embeddings, 30, MetricKind.Cos, exact=True)

    #We assume only the document associated with the query is relevant
    y_true = (np.expand_dims(np.arange(query_embeddings.shape[0]), 1) == matches.keys).astype(np.float32)
    y_pred = matches.distances * -1

    ndcg_scores = OrderedDict({
        "1": ndcg_score(y_true, y_pred, k=1),
        "3": ndcg_score(y_true, y_pred, k=3),
        "5": ndcg_score(y_true, y_pred, k=5),
        "10": ndcg_score(y_true, y_pred, k=10),
        "20": ndcg_score(y_true, y_pred, k=20),
        "30": ndcg_score(y_true, y_pred, k=30),
    })

    for k, v in ndcg_scores.items():
        print(f"NDCG@{k} Score: {v}")


if __name__ == '__main__':
    cli()