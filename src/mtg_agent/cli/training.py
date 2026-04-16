import click
from datasets import load_dataset
from peft import LoraConfig, TaskType
from sentence_transformers import SentenceTransformer, SentenceTransformerTrainingArguments, SentenceTransformerTrainer
from sentence_transformers.sentence_transformer.training_args import BatchSamplers, SentenceTransformerTrainingArguments
from sentence_transformers.sentence_transformer.losses import MultipleNegativesRankingLoss
from sentence_transformers.sentence_transformer.evaluation import InformationRetrievalEvaluator


@click.command()
def train():
    device = "cuda:0"
    model_name = "jinaai/jina-embeddings-v5-text-nano-retrieval"
    batch_size = 2
    query_prompt = "Instruct: Given a rule search query, retrieve relevant rule passages that answer the query\nQuery:"
    ds_path = "data/rules/mtg_rules_20260227_question_test.csv"
    test_size = 0.2

    model = SentenceTransformer(model_name, trust_remote_code=True)
    loss = MultipleNegativesRankingLoss(model)

    ds = load_dataset("csv", data_files=ds_path, split="train").train_test_split(test_size=test_size, seed=42)
    ds['train'] = ds['train'].filter(lambda s: len(s) < 5000, input_columns=["content"])

    queries = dict(zip(ds['test']['question_id'], ds['test']['question']))
    corpus = dict(zip(ds['test']['question_id'], ds['test']['content']))
    relevant_docs = {k: {k} for k in corpus.keys()}

    ir_eval = InformationRetrievalEvaluator(
        queries=queries,
        corpus=corpus,
        relevant_docs=relevant_docs,
        batch_size=4,
        name="MTG-valid"
    )
    res = ir_eval(model)
    print(res)

    ds = ds.select_columns(["content", "question"]).rename_columns({
        "content": "anchor",
        "question": "positive"
    })

    args = SentenceTransformerTrainingArguments(
        # Required parameter:
        output_dir="models/jina",
        # Optional training parameters:
        num_train_epochs=2,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=2e-5,
        warmup_steps=0.1,
        fp16=False,  # Set to False if you get an error that your GPU can't run on FP16
        bf16=False,  # Set to True if you have a GPU that supports BF16
        batch_sampler=BatchSamplers.NO_DUPLICATES,  # losses that use "in-batch negatives" benefit from no duplicates
        # Optional tracking/debugging parameters:
        eval_strategy="epoch",
        # eval_steps=100,
        save_strategy="epoch",
        # save_steps=100,
        save_total_limit=2,
        logging_steps=10,
        prompts={
            "query": "Query: ",
            "anchor": "Document: ",
        },
        gradient_accumulation_steps=4,
        # run_name="mpnet-base-all-nli-triplet",  # Will be used in W&B if `wandb` is installed
    )

    # model.add_adapter(LoraConfig(
    #     task_type=TaskType.FEATURE_EXTRACTION,
    #     inference_mode=False,
    #     r=4,
    #     lora_alpha=4,
    #     lora_dropout=0.1,
    # ))

    trainer = SentenceTransformerTrainer(
        model=model,
        args=args,
        train_dataset=ds['train'],
        eval_dataset=ds['test'],
        loss=loss,
        evaluator=ir_eval
    )
    trainer.train()

if __name__ == "__main__":
    train()