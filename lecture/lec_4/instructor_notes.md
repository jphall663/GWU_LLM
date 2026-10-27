# Instructor notes: Lecture 4

## Teaching boundary

Lecture 4 is about deciding what information reaches a model call and what the
application retains outside it. Retrieval mechanics belong to Lecture 5, while
tool invocation and agent loops belong to Lecture 6. Mention those components
as possible context sources without teaching their implementations here.

## Four terms that students should not conflate

- **Context** is the complete information supplied for one inference call.
- **History** is a record of prior interaction. It becomes context only when the
  application includes all or part of it in a request.
- **Persistent memory** is selected information retained across interactions.
  It is an application data product, not an automatic property of the model.
- **State** is the explicit set of variables that describes the application or
  task at a point in time and constrains valid transitions.

The model's learned parameters, attention key-value cache, API prompt cache,
conversation transcript, and application memory are also distinct. Prompt
caching may reduce the cost or latency of repeated prefixes; it neither selects
relevant information nor creates durable user memory.

## Context-window discussion

A published maximum context length is a capacity limit, not a recommendation to
fill every available token. Input, output, and—in reasoning models—reasoning
tokens share finite capacity. Longer inputs can cost more and take longer, and
relevant information may not be used uniformly across positions. The deck uses
a deliberately small teaching budget so selection decisions remain visible.

## Compression discussion

Recent-turn windows are transparent but forget early commitments. Summaries can
preserve older information compactly, but they are lossy derived records and may
introduce errors. Preserve unresolved questions, commitments, identifiers,
constraints, and provenance explicitly. Treat a summary as replaceable context,
not as the authoritative order record or case state.

## Persistent-memory discussion

Do not save every utterance. A defensible lifecycle is propose, confirm, save,
retrieve, update, and delete. Store the minimum useful structured fact with its
subject, provenance, confirmation status, timestamp, and expiry or review rule.
Enforce tenant or customer isolation before retrieval. Users need a way to see,
correct, and remove retained information.

## Notebook interpretation

The notebook deliberately combines model-mediated demonstrations with
deterministic checks. Generated answers illustrate the effect of assembled
context but can vary by model and date. The deterministic assertions test
application-owned invariants: budget compliance, customer isolation, memory
correction, required state fields, and valid transitions. Neither set alone is
enough for a production claim.

The JSON file contains only synthetic customer identifiers and preferences. Its
plain-text format is chosen for inspection, not as a production security model.
A deployed system would require authentication, authorization, encryption,
retention controls, audit logs, concurrency handling, and an approved privacy
design.

## Facilitation cautions

- Do not describe a model as remembering merely because prior text is resent.
- Do not let generated summaries overwrite authoritative business records.
- Ask who is allowed to write, retrieve, correct, and delete each memory field.
- When comparing focused and overloaded requests, discuss both correctness and
  input-token use; one successful sample does not establish robustness.
- Require test cases that switch customers and correct old facts, not only cases
  that reward successful recall.
