# DNSC 6290: LLMs: Concepts and Applications

Materials for a technical, nuts-and-bolts course on large language models,
their applications, and their evaluation.

## DNSC 6290: Course outline

1. [LLM and transformer foundations](#lecture-1-llm-and-transformer-foundations)
2. [Prompting and prompt development](#lecture-2-prompting-and-prompt-development)
3. [Model APIs, structured outputs, and typed decisions](#lecture-3-model-apis-structured-outputs-and-typed-decisions)
4. [Context engineering, memory, and state](#lecture-4-context-engineering-memory-and-state)
5. [RAG and knowledge pipelines](#lecture-5-rag-and-knowledge-pipelines)
6. [Tool use and agentic workflows](#lecture-6-tool-use-and-agentic-workflows)
7. [TEVV for LLM applications](#lecture-7-tevv-for-llm-applications)

Corrections or suggestions? Please [open an issue](https://github.com/jphall663/GWU_LLM/issues).

---

## Preliminary materials

- [Whiteboard notation](https://docs.google.com/presentation/d/1Axf9dizaE3XvGRelBHfsnAlMUPFuMExQ2WNVwQBKMrw/edit?usp=sharing)
- [Software configuration](#software-configuration)

## Lecture 1: LLM and transformer foundations

Tokens, embeddings, attention, transformers, generation; reasoning models and inference-time reasoning.

![An encoder--decoder transformer stacks attention and feed-forward blocks to transform token representations into vocabulary predictions.](lecture/lec_1/asset/transformer_basics.jpg)

<sub><sup>Transformer encoder and decoder stacks with attention and feed-forward blocks. **Source:** Adapted from [Vaswani et al. (2017), *Attention Is All You Need*](https://arxiv.org/abs/1706.03762).</sup></sub>

### Lecture 1 class materials

- [Lecture slides](lecture/lec_1/lecture_1.pdf)
- **Software example:** [Predicting the next word](https://github.com/jphall663/GWU_LLM/blob/main/lecture/lec_1/next_word_primer.ipynb)

## Lecture 2: Prompting and prompt development

Instructions, system prompts, examples/in-context learning, templates, task
decomposition, and iterative refinement.

![A prompt-development lifecycle moves from goal framing to design, examples or workflow stages, evaluation, and monitored release.](lecture/lec_2/asset/prompt-development-lifecycle.png)

<sub><sup>Prompt development should make task framing, reusable structure, comparison, and monitored release explicit. **Source:** Adapted from [Brown et al. (2020), *Language Models Are Few-Shot Learners*](https://proceedings.neurips.cc/paper_files/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf), [Bach et al. (2022), *PromptSource*](https://github.com/bigscience-workshop/promptsource), and [Zhu et al. (2024), *PromptBench*](https://arxiv.org/abs/2312.07910).</sup></sub>

### Lecture 2 class materials

- [Lecture slides](lecture/lec_2/lecture_2.pdf)
- **Software example:** [Practical prompt development](https://github.com/jphall663/GWU_LLM/blob/main/lecture/lec_2/prompt_development.ipynb)
- [Example goal prompt](https://github.com/jphall663/GWU_LLM/blob/main/lecture/lec_2/goal_prompt.md)

## Lecture 3: Model APIs, structured outputs, and typed decisions

Requests/responses, parameters, streaming, error handling; JSON schemas,
Pydantic validation, and Jev-style typed decisions.

![Four stacked controls for a reliable model API application: bound the request, validate data, bound the decision, and test claims.](lecture/lec_3/asset/api_guidelines.png)

<sub><sup>Reliable model API applications layer bounded requests, validated data, controlled decisions, and evaluation. **Source:** Course diagram, adapted from Lecture 3; API concepts follow [OpenAI (2026), *Text generation*](https://developers.openai.com/api/docs/guides/text?lang=python) and risk-management context follows [NIST (2024), *Generative AI Profile*](https://doi.org/10.6028/NIST.AI.600-1).</sup></sub>

### Lecture 3 class materials

- [Lecture slides](lecture/lec_3/lecture_3.pdf)
- **Software example:** [Model APIs, structured outputs, and typed decisions](https://github.com/jphall663/GWU_LLM/blob/main/lecture/lec_3/model_apis_structured_outputs.ipynb)

## Lecture 4: Context engineering, memory, and state

Context assembly, windows and budgets, conversation history, persistent
memory, and state management.

![Conversation history, persistent memory, and task state pass through selection, validation, ordering, and budgeting before becoming context for one model call.](lecture/lec_4/asset/context-engineering-memory-state.png)

<sub><sup>History, persistent memory, and application state become current-call context only when selected and budgeted. **Source:** Patrick Hall (2026), *Lecture 4: Context Engineering, Memory, and State*; memory architecture informed by [Packer et al. (2023), *MemGPT: Towards LLMs as Operating Systems*](https://arxiv.org/abs/2310.08560).</sup></sub>

### Lecture 4 class materials

- [Lecture slides](lecture/lec_4/lecture_4.pdf)
- **Software example:** [Context engineering, memory, and state](https://github.com/jphall663/GWU_LLM/blob/main/lecture/lec_4/context_engineering.ipynb)

## Lecture 5: RAG and knowledge pipelines

Ingestion, chunking, retrieval embeddings, vector/hybrid search, reranking,
grounded answers, and citations.

![A retrieval-augmented generation diagram shows a user query retrieving relevant documents, adding them to the LLM context, and producing a grounded answer.](lecture/lec_5/asset/rag_learning.jpg)

<sub><sup>RAG retrieves relevant documents, adds them to the model context, and grounds the resulting answer in the selected sources. <strong>Source:</strong> Patrick Hall, <a href="https://github.com/jphall663/GWU_LLM/blob/main/misc/existing_materials/06_GAI%20Learning%20-%20RAG.jpg"><em>GAI Learning: Retrieval-Augmented Generation</em></a>.</sup></sub>

### Lecture 5 class materials

- [Lecture slides](lecture/lec_5/lecture_5.pdf)
- **Software example:** [Cited RAG over NIST AI RMF actions](https://github.com/jphall663/GWU_LLM/blob/main/lecture/lec_5/rag_pipeline.ipynb)

## Lecture 6: Tool use and agentic workflows

Function calling, external connectivity, MCP, bounded agent loops,
orchestration, and agent identity; Text2SQL as a worked example.

![A model requests a tool, application code validates permissions and limits, and tool results return as observations before the next step.](lecture/lec_6/asset/bounded-agent-loop.svg)

<sub><sup>A bounded agent selects operations while application code controls execution, permissions, and termination. **Source:** Patrick Hall (2026), *Lecture 6: Tool Use and Agentic Workflows*; action–observation pattern informed by [Yao et al. (2023), *ReAct*](https://arxiv.org/abs/2210.03629).</sup></sub>

### Lecture 6 class materials

- [Lecture slides](lecture/lec_6/lecture_6.pdf)
- **Software examples:**
  - [Text2SQL: fixed workflows and bounded agents](https://github.com/jphall663/GWU_LLM/blob/main/lecture/lec_6/text_to_sql.ipynb)
  - [Local MCP calculator](https://github.com/jphall663/GWU_LLM/blob/main/lecture/lec_6/mcp_calculator.ipynb)
- [Setup and server startup](lecture/lec_6/README.md)

## Lecture 7: TEVV for LLM applications

Measurement science, benchmarks and their limitations, LLM judges, embedding-
and classifier-based tests, red teaming, field testing, human review, and
validation of AI measurement instruments.

![A model-testing workflow combines benchmark cases with embedding-based diagnostics and human-interpretable evidence.](lecture/lec_7/asset/model-testing-benchmarks-and-embeddings.png)

<sub><sup>Benchmark and embedding-based model testing should support a stated construct and decision rather than a leaderboard alone. **Source:** Sudjianto et al. (2024), [*Human-Calibrated Automated Testing and Validation of Generative Language Models*](https://arxiv.org/pdf/2411.16391).</sup></sub>

### Lecture 7 class materials

- [Lecture slides](lecture/lec_7/lecture_7.pdf)
- **Software examples:**
  - [Simple benchmark and embedding tests](https://github.com/jphall663/GWU_LLM/blob/main/lecture/lec_7/benchmark_embeddings.ipynb)
  - [LLM-as-a-judge validation](https://github.com/jphall663/GWU_LLM/blob/main/lecture/lec_7/llm_as_judge.ipynb)
  - [Bounded red-teaming examples](https://github.com/jphall663/GWU_LLM/blob/main/lecture/lec_7/red_teaming.ipynb)

## Software configuration

The examples use Python 3.13 and the locked project environment. From the
repository root, install [uv](https://docs.astral.sh/uv/getting-started/installation/)
and run:

```bash
uv sync --locked
```

The [project README](README.md) covers environment setup. Lecture 1's setup
notes include optional NVIDIA GPU acceleration.

---

This project is maintained by [jphall663](https://github.com/jphall663).
