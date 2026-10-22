# Lecture 5 instructor notes

## Teaching arc

Begin with a decision a knowledge system must support, then distinguish an LLM's
parameterized knowledge from an external, attributable corpus. Move in order
through ingestion, chunking, retrieval, reranking, and grounded generation.
End by treating citations as inspectable links between claims and sources, not
as proof that the claim is entailed.

## Notebook discussion points

The notebook uses only eleven short NIST AI RMF records so that every source,
score, and model decision is visible. It is not a realistic retrieval
evaluation. Ask students why the lexical top result and dense top result differ,
then show how reciprocal-rank fusion preserves candidates from both lists.

The structured reranker uses an LLM judge to choose three chunks from six
candidates. The LLM receives the question and retrieved chunks, then returns a
structured relevance ranking before a separate LLM call generates the answer.
Its rationale is useful for debugging, but it does not establish correctness.
The final answer's source-ID validation only ensures that citations name
selected chunks; students should still compare each sentence with the cited text
for entailment and completeness.

## Corpus-specific semantic chunking

The AI RMF example corpus already separates content into named subcategories.
For this corpus, use one subcategory record as one semantic chunk and retain its
source ID and URL. A generic text splitter would add complexity without creating
a more meaningful retrieval unit. Split a record further only when it is too
long for the retrieval or context budget, or when the source lacks useful
structural boundaries.

## Chunking tradeoff

Shorter chunks generally improve retrieval of specific details and make
citations more local to the supporting text. Larger chunks preserve more
cross-sentence and cross-section context, which can better support thematic
questions and summarization. This is a hypothesis to test on representative
queries, not a universal rule: document structure, retrieval depth, and the
model context budget can change the preferred size.

## Reciprocal-rank fusion

Reciprocal-rank fusion (RRF) combines ranked lists, not the raw BM25 and cosine
scores. For each retriever, a chunk at rank $r$ receives $1/(k+r)$; the notebook
uses $k=60$, the conventional damping constant. Sum that small contribution
across the lexical and dense lists. Thus, a chunk supported by both retrieval
methods can rise above a chunk that scores extremely well only in one method.

RRF is a useful teaching baseline because BM25 and cosine similarity are on
different numeric scales, so directly adding their raw values is usually hard
to justify. It also has limitations: it discards score magnitudes and treats
every rank list equally. Tune the candidate depth and $k$ on held-out queries,
then compare RRF to a calibrated weighted-score or learned-ranking baseline.

## Hybrid retrieval and GraphRAG

Slide 8 is an appropriate place to introduce GraphRAG as a third retrieval
path alongside lexical and dense retrieval. A graph-based approach can retrieve
connected entities, relationships, or communities when the answer depends on
links across passages rather than one similar chunk. Emphasize that it is not a
free accuracy upgrade: graph extraction, indexing, and maintenance add cost and
can introduce their own errors. Microsoft describes GraphRAG as a structured,
hierarchical approach that extracts a knowledge graph from text and uses
community summaries for RAG tasks.

## Reranking techniques

Reranking is a second-stage decision: retrieve a broader, inexpensive candidate
set first, then spend more computation deciding which few passages belong in
the prompt. A cross-encoder is the standard baseline. Unlike a bi-encoder,
which embeds the query and document separately for fast similarity search, a
cross-encoder processes one query--document pair together and predicts a
relevance score from their joint representation. This makes it slower but
better able to recognize precise matches, negation, and query-specific context.

Useful techniques to contrast are:

- A cross-encoder scores every query--candidate pair independently (a
  pointwise score); it is a strong, practical default for a small top-$k$.
- Pairwise learning-to-rank compares two candidates for the same query and
  learns which should rank higher. Listwise methods instead optimize the order
  of an entire candidate list.
- Late-interaction models such as ColBERT retain token-level representations,
  offering a middle ground between a single-vector retriever and a full
  cross-encoder.
- An LLM reranker can score candidates one at a time, compare pairs, or order a
  list. It can use richer task instructions, but cost, latency, output-format
  variability, and evaluation requirements are substantially higher.

The slide's phrase “pairwise scorer” describes a query paired with a candidate
for scoring. Strictly, this differs from pairwise learning-to-rank, which
compares two candidates against each other. Keep that distinction explicit when
students encounter both terms. Evaluate rerankers beyond ranking metrics: use
held-out questions and check whether the selected evidence supports the final
answer.

## Tool examples: Gemini Notebook and AnythingLLM

Slide 12 is an appropriate place to mention end-user RAG tools, provided they
are presented as examples of a product layer rather than as the architecture.
As of October 2026, Google has renamed NotebookLM to **Gemini Notebook**;
“Gemini Notebook (formerly NotebookLM)” will be clearest for students who know
the older name. It is a source-grounded research and learning product with
citations, not a substitute for specifying an authorized corpus, evaluating
retrieval, or checking entailment.

AnythingLLM is also current. Its desktop documentation describes a local,
single-user application that can combine local or cloud models with documents,
RAG, and agents; its Docker deployment is the relevant comparison when multiple
people need shared access. Use it to contrast a configurable/local-first tool
with Gemini Notebook's managed product experience. Neither tool should be
presented as a production architecture by itself: source permissions, model
data handling, index lifecycle, audit logging, evaluation, and deployment
controls remain design responsibilities.

## Organizing the tools slide

For Slide 12, prefer three columns—SDKs, frameworks, and products—over placing
tool names inside the RAG-stage diagram. The diagram answers “what stages does a
RAG system contain?” whereas the columns answer “at what abstraction layer does
a tool operate?” A direct SDK, a framework, and an end-user product can each
span several or all stages, so assigning them to individual stage boxes creates
a misleading one-to-one mapping. If visual orientation is useful, retain a very
small, unlabeled pipeline strip above the columns, but make the columns the
slide's visual and instructional center.

## Summary visual

The closing slide uses Patrick Hall's *GAI Learning: Retrieval-Augmented
Generation* diagram as a high-level synthesis. Use it to revisit the four
observable handoffs: authorized source material to chunks, chunks to ranked
evidence, evidence to the context window, and the generated answer back to
verifiable sources. The diagram is intentionally broad; the preceding slides
and notebook provide the implementation-level choices and evaluation checks.

## Facilitation cautions

The example corpus is public NIST material. A real organization must authorize
each source, preserve access controls through retrieval, and avoid sending data
to a model provider unless its data-handling terms and the organization's policy
permit it. Corpus refreshes, embedding-model changes, chunking changes, and
retrieval changes can alter answers and require regression evaluation.
