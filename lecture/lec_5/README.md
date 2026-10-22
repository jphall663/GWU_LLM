# Lecture 5: RAG and knowledge pipelines

The slide deck introduces retrieval-augmented generation (RAG) as an
inspectable knowledge pipeline: ingestion, chunking, embeddings, lexical and
hybrid retrieval, reranking, grounded generation, citations, and operational
tool-chain choices.

## Reproducible environment

From the repository root:

```bash
uv sync --locked
```

Set the direct OpenAI API key in the ignored root `.env` file:

```dotenv
OPENAI_API_KEY=your-key-here
```

The notebook uses a secure `getpass` fallback when the environment variable is
absent. Optional model overrides are `OPENAI_TEXT_MODEL` and
`OPENAI_EMBEDDING_MODEL`.

## Run the RAG example

```bash
uv run jupyter lab lecture/lec_5/
```

`rag_pipeline.ipynb` uses an attributed, small NIST AI RMF corpus. It treats
each AI RMF subcategory record as one semantic chunk, compares BM25 and
cosine-similarity retrieval, fuses their rankings, reranks six candidates with
a structured model response, and produces a source-ID-cited answer. The example
is intentionally transparent rather than a production retrieval service.

## Build the slides

```bash
cd lecture/lec_5
latexmk -pdf -interaction=nonstopmode -halt-on-error lecture_5.tex
```

The selected bibliography is in `references.bib`; the example corpus is in
`data/rmf_rag_corpus.csv`.
