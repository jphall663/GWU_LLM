# Lecture 7: TEVV for LLM applications

The slide deck introduces measurement science, model testing, benchmark
limitations, LLM-as-a-judge, embeddings and classifiers, red teaming, field
testing, and validation of AI measurement instruments. It uses the GW Beamer
template, cited NIST and academic sources, and source-attributed teaching
visuals.

## Reproducible environment

From the repository root:

```bash
uv sync --locked
```

Place the direct OpenAI API key in the ignored root `.env` file:

```dotenv
OPENAI_API_KEY=your-key-here
```

The notebooks also use a secure `getpass` fallback when the environment
variable is absent. Optional model overrides are `OPENAI_TEXT_MODEL`,
`OPENAI_EMBEDDING_MODEL`, `OPENAI_JUDGE_MODEL`, and `OPENAI_RED_TEAM_MODEL`.

## Run the examples

```bash
uv run jupyter lab lecture/lec_7/
```

### VS Code

JupyterLab is optional. After `uv sync --locked`, open the repository root in
VS Code with Microsoft's Python and Jupyter extensions installed. Open any
Lecture 7 notebook; in **Select Kernel**, choose **Select Another Kernel...** →
**Python Environments** → `.venv/bin/python` (macOS/Linux) or
`.venv\Scripts\python.exe` (Windows), then run the cells in order. See the
[root VS Code setup](../../README.md#run-notebooks-in-vs-code) for details.

The three notebooks are:

- `benchmark_embeddings.ipynb`: a transparent multiple-choice benchmark,
  Wilson interval, slice analysis, embedding-based intent classifier, and 2-D
  PCA view of the embedding space.
- `llm_as_judge.ipynb`: a structured rubric, repeated judgments, and comparison
  with small human reference ratings.
- `red_teaming.ipynb`: bounded prompt-injection tests, a synthetic canary,
  attack-success reporting, and a counterfactual consistency probe.

## Build the slides

```bash
cd lecture/lec_7
latexmk -pdf -interaction=nonstopmode -halt-on-error lecture_7.tex
```

The deck's complete, self-contained bibliography is stored in `references.bib`.
