# Lecture 3: Model APIs, structured outputs, and typed decisions

Lecture 3 introduces the practical boundary between an LLM application and a
model service: request configuration, response metadata, latency and rate
limits, streaming, bounded failure handling, JSON Schema, Pydantic data
contracts, typed decisions, abstention, escalation, and evaluation.

## Reproducible environment

From the repository root, install the locked environment:

```bash
uv sync --locked
```

Create a repository-root `.env` file containing an OpenAI API key. The file is
ignored by Git. The notebook uses an interactive `getpass` fallback if the key
is absent.

```dotenv
OPENAI_API_KEY=your_key_here
```

## Run the example

The example makes live API calls, including two configuration comparisons,
streaming, structured extraction, typed triage, and a three-case evaluation.
Review the model name and API charges before running it.
The lecture-local utils.py contains the small, reusable bounded-retry decorator
used in the failure-handling section.

```bash
uv run jupyter lab lecture/lec_3/model_apis_structured_outputs.ipynb
```

### VS Code

JupyterLab is optional. After `uv sync --locked`, open the repository root in
VS Code with Microsoft's Python and Jupyter extensions installed. Open
`model_apis_structured_outputs.ipynb`; in **Select Kernel**, choose **Select
Another Kernel...** → **Python Environments** → `.venv/bin/python`
(macOS/Linux) or `.venv\Scripts\python.exe` (Windows), then run the cells in
order. See the [root VS Code setup](../../README.md#run-notebooks-in-vs-code)
for details.

## Build the slides

The slide deck uses Biber for citations. Run the command from this directory:

```bash
cd lecture/lec_3
latexmk -pdf lecture_3.tex
```
