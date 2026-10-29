# DNSC 6290: LLMs: Concepts and Applications

A 1.5 credit graduate class about the nuts and bolts of LLMs.

## Course site

The repository root is a GitHub Pages site, configured in `_config.yml` and
published at <https://jphall663.github.io/GWU_LLM/>. Its landing page links the
available lecture materials and the course outline.

# Setting for code examples

## Install `uv`

```bash
# macOS (requires Homebrew)
brew install uv

# Ubuntu
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Learn more about [uv](https://docs.astral.sh/uv/getting-started/installation/).

## Install Python 3.13

```bash
uv python install 3.13
uv python pin 3.13
uv venv
source .venv/bin/activate
python --version
```

## Lecture environments

Install the locked project dependencies from the repository root:

```bash
uv sync --locked
```

Individual lectures may have additional setup notes. Lecture 1 now combines
the next-token MLP example with transformer concepts, a plain-language summary,
canonical references, and the Promontory AI GWU practicum guest lecture; its setup notes also cover
optional NVIDIA GPU acceleration. See [lecture 1](lecture/lec_1/README.md).

Lecture 2 covers prompting and prompt development with a GW Beamer deck, a
direct-OpenAI-API notebook that compares zero-shot and few-shot routing prompts,
and an example bounded goal prompt for a course-grounded chat assistant. See
[lecture 2](lecture/lec_2/README.md).

Lecture 3 covers model APIs, structured outputs, and typed decisions with a GW
Beamer deck and a direct-OpenAI-API notebook. The example inspects request and
response metadata, compares operating settings, streams output, validates
Pydantic-backed structured data, routes a typed complaint-triage decision, and
evaluates it against labeled cases. See [lecture 3](lecture/lec_3/README.md).

Lecture 4 covers context engineering, memory, and state with a GW Beamer deck
and a direct-OpenAI-API notebook. The example separates conversation history,
persistent customer memory, case state, and current-call context; measures exact
input tokens; enforces a teaching budget; compares history strategies and
context quality; persists synthetic, customer-isolated JSON memory; and tests
application invariants. See [lecture 4](lecture/lec_4/README.md).

Lecture 5 covers retrieval-augmented generation (RAG) and knowledge pipelines,
with a GW Beamer deck and a direct-OpenAI-API notebook that demonstrates
attributed ingestion, subcategory-based semantic chunking, lexical and embedding
retrieval, hybrid ranking, reranking, and cited answers. See [lecture 5](lecture/lec_5/README.md).

Lecture 6 covers tool use and agentic workflows with a GW Beamer deck and two
direct-OpenAI-API notebooks: a fixed versus bounded-agent Text2SQL comparison
over synthetic SQLite sales data, and tool discovery/invocation through a
separate local MCP calculator server. The shared lockfile includes the MCP v1
SDK; see [lecture 6](lecture/lec_6/README.md) for startup and execution commands.

Lecture 7 covers AI test, evaluation, verification, and validation (TEVV), with
a GW Beamer deck and three executable examples for benchmarks, embeddings, and
a 2-D embedding view; LLM-as-a-judge validation; and bounded red teaming. The
examples use the direct OpenAI API. Add `OPENAI_API_KEY` to an ignored
repository-root `.env` file, then run `uv sync --locked`; see [lecture 7](lecture/lec_7/README.md)
for commands.

The lockfile is cross-platform: standard TensorFlow is installed on macOS and
the `and-cuda` extra is installed on Linux for compatible NVIDIA environments.

