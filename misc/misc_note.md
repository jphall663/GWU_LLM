## Preliminaries

#### 7 lecture flow

| #   | Lecture                                                 | Core coverage                                                                                                                         |
| --- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **LLM and transformer foundations**                     | Tokens, embeddings, attention, transformers, generation; capabilities and limitations; reasoning models and inference-time reasoning. |
| 2   | **Prompting and prompt development**                    | Instructions, system prompts, examples/in-context learning, templates, task decomposition, and iterative refinement.                  |
| 3   | **Model APIs, structured outputs, and typed decisions** | Requests/responses, parameters, streaming, error handling; JSON schemas, Pydantic validation, and Jev-style typed decisions.          |
| 4   | **Context engineering, memory, and state**              | Context assembly, windows and budgets, conversation history, persistent memory, and state management.                                 |
| 5   | **RAG and knowledge pipelines**                         | Ingestion, chunking, retrieval embeddings, vector/hybrid search, reranking, grounded answers, and citations.                          |
| 6   | **Tool use and agentic workflows**                      | Function calling, external connectivity, MCP, bounded agent loops, and orchestration; **Text2SQL** as a worked example.               |
| 7   | **TEVV for LLM applications**                           | Test datasets, component/end-to-end evaluation, correctness, LLM judges, human review, regression testing, and error analysis.        |

#### 6 lecture flow

| #   | Lecture                                                 | Core coverage                                                                                                                         |
| --- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **LLM and transformer foundations**                     | Tokens, embeddings, attention, transformers, generation; capabilities and limitations; reasoning models and inference-time reasoning. |
| 2   | **Prompting and context engineering**                   | Instructions, examples/ICL, templates, iterative refinement; context assembly and budgets, conversation history, memory, and state.   |
| 3   | **Model APIs, structured outputs, and typed decisions** | Requests/responses, parameters, streaming, error handling; JSON schemas, Pydantic validation, and Jev-style typed decisions.          |
| 4   | **RAG and knowledge pipelines**                         | Ingestion, chunking, retrieval embeddings, vector/hybrid search, reranking, grounded answers, and citations.                          |
| 5   | **Tool use and agentic workflows**                      | Function calling, external connectivity, MCP, bounded agent loops, and orchestration; **Text2SQL** as a worked example.               |
| 6   | **TEVV for LLM applications**                           | Test datasets, component/end-to-end evaluation, correctness, LLM judges, human review, regression testing, and error analysis.        |
| —   | **Final exam**                                          | Applied scenarios: select an architecture, diagnose failures, interpret outputs, and design appropriate tests.                        |

### Lecture 1

#### Opener

Combine:

- https://colab.research.google.com/drive/1ZZTHU8k0B2EB9oxibLN0F47AAdnH86IG
- IMG_6261.jpg

into a coherent opener on predicting the next word. 

Additional conceptual topics: 

- tokens

- embeddings 

- attention

- transformers

- generation 

- "reasoning"

- inference time compute/inference scaling

- alignment processes