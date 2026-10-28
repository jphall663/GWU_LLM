# Instructor notes: Lecture 4

## Teaching boundary

Lecture 4 is about deciding what information reaches a model call and what the
application retains outside it. Retrieval mechanics belong to Lecture 5, while
tool invocation and agent loops belong to Lecture 6. Mention those components
as possible context sources without teaching their implementations here.

## Section title: the information boundary

“The information boundary” refers to the application-controlled boundary
between all information that exists—history, memory, state, policies, and other
records—and the subset assembled for one model call. The phrase is conceptually
accurate, but it asks students to infer that definition before the section has
established it.

Clearer alternatives include:

- **What the model sees** — concise and immediately understandable; the slides
  can then explain that the application constructs this view.
- **Selecting information for a model call** — the most explicit description of
  the application action emphasized by the section.
- **From stored information to model context** — foregrounds the distinction
  between application-held data and current-call context.
- **Inside and outside the model call** — makes the boundary metaphor concrete,
  although it is slightly less technical.
- **The context boundary** — preserves the boundary concept while naming the
  relevant object more directly.
- **What becomes context—and what does not** — closely matches the section's
  distinction among history, memory, state, and selected context.

The strongest concise replacement is **What the model sees**. For a more
technical title, prefer **From stored information to model context**.

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
caching lets a provider reuse processing for an unchanged prompt prefix and may
reduce the cost or latency of later calls. It is not a conversation strategy:
full history, recent turns, and summary-plus-recent change which content the
application sends, whereas caching changes how repeated content is processed.
It neither selects relevant information nor creates, retrieves, or summarizes
history, memory, or state.

## Context-window discussion

A published maximum context length is a capacity limit, not a recommendation to
fill every available token. Input, output, and—in reasoning models—reasoning
tokens share finite capacity. Longer inputs can cost more and take longer, and
relevant information may not be used uniformly across positions. The deck uses
a deliberately small teaching budget so selection decisions remain visible.

The slide title **“A context window is a finite capacity, not a quality target”**
means that the window is an upper bound on the tokens available to a request,
not a target utilization level and not a measure of answer quality. Filling more
of the window does not inherently improve an answer; additional material may be
irrelevant, stale, conflicting, or distracting. Context engineering instead
aims to supply the smallest sufficient set of authoritative information while
reserving capacity for output, reasoning when applicable, and a safety margin.

Less normative, more instructive title alternatives include:

- **A context window sets a shared token budget** — concise and directly tied
  to both the equation and allocation diagram.
- **Context-window capacity is shared across request components** — emphasizes
  that instructions, data, history, output, and reasoning compete for capacity.
- **A context window accommodates input, output, and reasoning** — names the
  main categories represented in the equation.
- **Token budgeting allocates context-window capacity** — foregrounds the
  application design task.
- **How a context window is allocated** — accessible and descriptive, although
  less specific about what is being allocated.
- **Context windows constrain information available to a model call** — links
  capacity to the lecture's larger information-boundary theme.

The strongest replacement for this slide is **A context window sets a shared
token budget**. It describes the concept without implying that students have
already adopted an undesirable optimization target.

In the capacity diagram, **slack** and **safety margin** refer to the same gray
segment: capacity deliberately left unallocated after budgeting rules, data,
history, and output. This margin absorbs estimation error and usage variability
and helps prevent a request from reaching the hard context-window limit. It is
separate from reserved output capacity. “Safety margin” is the clearer label
because “slack” can imply capacity left over accidentally rather than capacity
reserved intentionally.

On the focused-versus-overloaded request slide, the **“?” segment represents the
current user question**, not a safety margin. The safety margin appears only as
the gray segment in the earlier capacity-allocation diagram. Labeling the final
request segment “question” or “input” is clearer than using a question mark.

## Compression discussion

Recent-turn windows are transparent but forget early commitments. Summaries can
preserve older information compactly, but they are lossy derived records and may
introduce errors. Preserve unresolved questions, commitments, identifiers,
constraints, and provenance explicitly. Treat a summary as replaceable context,
not as the authoritative order record or case state.

## Persistent-memory discussion

Do not save every utterance. Explicit persistent-memory management processes
include propose, confirm, save, retrieve, update, and delete. Store the minimum useful structured fact with its
subject, provenance, confirmation status, timestamp, and expiry or review rule.
Enforce tenant or customer isolation before retrieval. Users need a way to see,
correct, and remove retained information.

Use **session memory** for short-term working information that expires with the
session, and **persistent memory** for selected information retained across
sessions. Some memory architectures place both under a broad memory hierarchy,
but calling both “persistent” obscures their different lifetimes, controls, and
privacy implications.

Prefer **long-term storage** over **database** in the slide label. A database is
one possible persistence mechanism, but persistent memory can also be backed by
a file, key-value store, document store, or other application-managed system.
The companion notebook deliberately uses an inspectable JSON file.

On the right side of the session-versus-persistent-memory slide, the two boxes
contrast representations of a persistent preference. The **structured record**
identifies the subject and field, stores a specific value, records confirmation,
and includes an update timestamp; an application can retrieve, validate, audit,
correct, or delete it deterministically. The **unstructured note** expresses a
similar idea in vague prose without a clear field, confirmation status, or
provenance. It is harder to interpret safely and may overstate what the user
actually approved. Clearer slide labels would be **Preferred: structured
persistent record** and **Ambiguous: unstructured prose note**.

In the phrase **“X invariant,”** an invariant is a property about X that must
remain true across every request, retrieval, and valid state transition. It is
an application-enforced condition, not a probabilistic model preference. The
isolation invariant means a request for customer A must never return customer
B's records. The privacy box, however, lists several design and governance
requirements—data minimization, purpose and provenance, access, retention,
correction, and deletion—rather than one precisely testable invariant. For a
general audience, **Isolation requirement** and **Privacy requirements** are
clearer labels; reserve “invariant” for a property that can be stated and tested
as always true.

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
