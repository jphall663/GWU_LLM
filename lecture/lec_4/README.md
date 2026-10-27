# Lecture 4: Context engineering, memory, and state

Lecture 4 treats model input as an engineered application boundary. The slide
deck and notebook distinguish current-call context, conversation history,
persistent memory, and explicit application state; then develop context
assembly, token budgets, compression, long-context limitations, memory
lifecycle controls, and evaluation.

## Reproducible environment

From the repository root:

```bash
uv sync --locked
```

Create an ignored repository-root `.env` file containing a direct OpenAI API
key. The notebook uses a secure `getpass` fallback when the variable is absent.

```dotenv
OPENAI_API_KEY=your-key-here
```

The optional `OPENAI_TEXT_MODEL` variable overrides the notebook's default
model, `gpt-5-mini`.

## Run the example

```bash
uv run jupyter lab lecture/lec_4/context_engineering.ipynb
```

The customer-support example uses synthetic records. It keeps conversation
history, persistent customer memory, case state, and the assembled request as
separate objects; displays the request before sending it; obtains exact token
counts from the Responses API; compares recent-only and summarized history;
contrasts overloaded and focused context; updates a customer-isolated JSON
memory store; and runs deterministic application-behavior checks. It imports
the bounded retry decorator from `lecture/lec_3/utils.py`.

Live calls consume API tokens. Review the selected model and account charges
before executing the notebook.

## Build the slides

The deck uses Biber for citations. Run from this directory:

```bash
cd lecture/lec_4
latexmk -pdf -interaction=nonstopmode -halt-on-error lecture_4.tex
```

The selective bibliography is in `references.bib`. Concise teaching guidance
and interpretation cautions are in `instructor_notes.md`.
