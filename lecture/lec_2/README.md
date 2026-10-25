# Lecture 2: Prompting and prompt development

The slide deck and notebook develop prompting as an inspectable engineering
practice: task framing, system boundaries, examples, templates, decomposition,
controlled revision, and prompt governance.

## Reproducible environment

From the repository root:

```bash
uv sync --locked
```

Set a direct OpenAI API key in the ignored root `.env` file:

```dotenv
OPENAI_API_KEY=your-key-here
```

The notebook uses `getpass` when the variable is absent. You may override the
model with `OPENAI_TEXT_MODEL`.

## Run the example

```bash
uv run jupyter lab lecture/lec_2/prompt_development.ipynb
```

The notebook compares zero-shot and few-shot classification prompts, renders a
versioned template, tests a refinement against a small held-out set, and
records the model and prompt versions used.

## Build the slides

```bash
cd lecture/lec_2
latexmk -pdf -interaction=nonstopmode -halt-on-error lecture_2.tex
```

`goal_prompt.md` is an example bounded implementation goal for a coding agent
building a course-grounded chat assistant.
