# Lecture 6 instructor notes

## Teaching sequence

Begin with an operation the business needs: an authorized read or calculation,
then distinguish requesting an action from executing it. Revisit Lecture 3's
structured-output versus business-valid-decision distinction and Lecture 4's
explicit state. RAG in Lecture 5 supplied evidence; tools can obtain evidence
and also act on systems. This creates an execution boundary. Lecture 7 extends
the small evaluation into systematic TEVV.

Use the 18-content-slide sequence in `lecture_6.tex`. The Text2SQL example
supports the concepts throughout, with the calculator confined to the two
connectivity/MCP slides. Introduce multi-agent handoffs conceptually; a second
agent is unnecessary for the notebook's small analytics task.

## What distinguishes a tool, workflow, and agent?

A tool implements an operation. A fixed workflow chooses the sequence in code;
its model may still choose a SQL statement or a typed stop decision. In an
agent, the model chooses some next steps based on feedback, while the host
retains tool permissions and limits. Tool calling alone does not imply a
general autonomous agent. A framework is optional: the short loop makes the
control flow and its stop conditions inspectable.

## Why these business definitions?

Freeze the reference date at 2026-10-15 so last quarter never changes with the
execution date. Use a half-open interval, 2026-07-01 <= date < 2026-10-01, to
include all of September and exclude October 1. ISO dates sort correctly here;
a production source may need explicit timezone and timestamp handling.

Net sales are item quantity times unit price minus the total discount for that
line. All stored money is integer cents; divide the final sum by 100.0. Missing
discounts mean zero by explicit fixture convention, not by a universal rule.
Missing regions form an Unknown group. Only completed orders count. Profit
cannot be derived without costs. "Best customers" needs a metric and period.

Manually derived regional totals are East 240 + 180 = 420, West 300, South 90,
and Unknown 40 USD. East has two completed orders and three line items; other
included regions have one order each. The cancelled South order, pending West
order, June 30 order, and October 1 order are excluded. These fixtures expose
status, boundary, join-grain, and missing-value mistakes.

## Why does a SELECT-prefix check not suffice?

SQL text checks do not establish authorization, prevent expensive reads, or
restrict access to sensitive tables. The executor opens a fresh read-only
connection per call, enables query_only and trusted_schema controls, and uses
SQLite's authorizer to permit only SELECT/recursive operations, approved table
reads, and named functions. Everything else is denied, including PRAGMA,
ATTACH, mutations, schema changes, and extension loading. `execute` also rejects
multiple statements. SQLite can omit the database name on a COUNT(*) read;
the callback permits that only for an allowlisted table. Attachment is denied,
and the fresh connection has no attached databases or temporary objects.

The row cap limits output, not aggregate computation. Fetching one extra row
detects truncation; that result is not accepted as a full answer. A progress
callback cooperatively interrupts long queries; the notebook checks this using
an unbounded recursive aggregate. It is not an OS sandbox or a hard real-time
deadline. Production work needs authenticated authorization, resource-isolated
execution, appropriate data minimization, and stronger operational limits.

## How are loops bounded and errors handled?

The normal agent allows at most six tool calls, two tool errors, and seven
model calls. Incomplete API responses and API failures return explicit failed
runs; tool/error/model limits return limit_reached. No evidence-free or
truncated query may support completed status. Argument parsing and tool-name
validation happen independently of strict model schemas.

Tool results return with call_id, and the response output items are preserved
for the next call. The model can repair a missing column from the actual
SQLite feedback. The repair example deliberately inserts an invalid first
request, labels it instructor-seeded, and asks the live model to continue.
Explain that this tests a known failure path; it is not a naturally observed
model error or a fair accuracy comparison with the unseeded baseline.

## What does MCP add?

The notebook is the host; its ClientSession connects to a server process.
`list_tools` discovers the server contract; the host exposes only the approved
calculator to the model. The model returns a function request. The host
validates it and sends call_tool over MCP; the server computes; the host
returns the observation to the model. Direct OpenAI HTTP requests and local
MCP stdio messages are distinct connections. A locally spawned server is not
a remote hosted MCP endpoint.

The server never receives the host API key. Its stdout is protocol-only, and
the stdio client context starts and stops it. The calculator validates finite,
nonnegative revenues with a positive previous value; the notebook also checks
that the server rejects zero previous revenue. Use the same currency/scale
for both arguments. The formula is 100 * (current - previous) / previous = 25%.

The locked MCP dependency uses the v1 Python SDK interface, constrained below
v2 for reproducibility. The archived IBM diagram labels remote HTTP+SSE; its
caption explicitly identifies that older labeling and points students to the
current Streamable HTTP architecture. MCP discovery does not authenticate a
business user, grant permission, or guarantee correctness. Local subprocesses
run with host privileges; isolation is a separate deployment decision.

## What counts as a useful evaluation?

Hold data, definitions, model, and execution controls fixed. The fixed workflow
has one query attempt; the agent may spend extra calls on discovery and repair.
Count application-dispatched schema reads in the baseline's tool totals as well
as model-selected tool calls in the agent; the trace's source field makes this
distinction explicit. Token usage includes all calls within each run, and model
latency includes any SDK retry. Results are illustrative, not cost estimates.

The five cases compare independently derived result rows and expected stop
behavior. Reference results never enter the model prompts. Different valid SQL
can have equivalent results, so string equality is the wrong default metric.
Conversely, an incorrect query can accidentally match a small fixture. Check
joins, filters, grouping, and semantics and use additional datasets before
claiming correctness. Column aliases are ignored, but each region/value pairing
must remain correct. The tests preserve result order independence and numeric
type equivalence.

Model accuracy is an outcome, not an invariant. The notebook prints cases that
fail and their traces and keeps running, so a legitimate model mistake does
not hide the rest of the comparison. Deterministic execution/security checks,
main demonstrations, repair, and calculator correctness do have assertions.
Do not replace reference answers to fit observed model output. A development
run caught an agent returning a completed answer for an unavailable-profit
request; inspect for a substituted metric, invented costs, or an incorrect
status instead of counting a plausible explanation as success.

Review explanation quality separately: correct values, USD units, quarter,
completed-order exclusion, discount/Unknown handling, no unsupported causal
claims, and explicit uncertainty or missing information. The automated cases
check result correctness and behavior, not full explanation faithfulness.
Do not claim reliability from a single run on five synthetic cases. Repeat on
held-out questions and database variants and calibrate any automated grader.

## Security and oversight discussion

A malicious database value or tool description can attempt to redirect an
agent. Prompts help communicate the trust boundary, but connected-system
permissions enforce it even when the model is manipulated. The notebook
simulates a restricted table and directly attempts prohibited writes without
sending sensitive data to the provider. Its prompt-injection slide is an
illustrative scenario; the notebook does not claim comprehensive attack testing.

For consequential actions, display the exact proposed operation, target,
parameters, and evidence to an authorized reviewer. Bind approval to those
values and revalidate before execution. The example never permits a write and
does not implement an approval service. Redact sensitive data from logs and
minimize anything included in model context in a real deployment.

## Sources and provenance

Read the local inventory and Text2SQL baseline first. The baseline's Azure
connection and SELECT-prefix validator were replaced, while its short
question-to-SQL-to-execution teaching sequence was retained and credited in
the notebook. Other local notebook examples informed headers, root .env
loading, and direct API conventions. The course comparison workbook supplied
relevant GenAI for Business and SDSU CS 668 course links, which were inspected.
The Promontory practicum page was unavailable through the browsing tool during
preparation; its local catalog was consulted, and primary sources support the
actual lecture claims.

Reuse the existing Greshake (indirect injection) and Kraprayoon (governance)
BibTeX entries from library-cleaned.bib, validated against their arXiv records.
ReAct and Spider were absent from that pool, so add their canonical paper
metadata. The official OpenAI function-calling guide, MCP architecture and
v1 SDK, and SQLite authorizer/progress documentation support implementation.
Anthropic's 2024 workflow-pattern article supports design vocabulary, not a
claim about current managed-agent products.

The IBM architecture image is copied from `HR_AI_Exec_Ed.zip`'s
`img/model-context-protocol.png`, with IBM's named linked source retained.
The website's loop diagram is original course artwork, consistent with the
slide loop. Reference slides are explicit, top-aligned frames with identical
titles and scriptsize entries. All content-slide diagrams, code blocks, and
instructional tables have descriptions directly underneath.

## Verified execution snapshot (2026-10-29)

Both notebooks executed end to end using Python 3.13, the locked environment,
and direct OpenAI access with gpt-5-mini. Text2SQL's deterministic checks passed
for writes, private reads (including COUNT), ATTACH, PRAGMA, extension loading,
multiple statements, invalid arguments/tool names, truncation, and query
interruption. The seeded missing-column query was repaired to the reference
regional totals. Explicit tool/error-limit paths stopped unsuccessfully as
expected. After making connection cleanup explicit, the database setup,
contracts, controls, and temporary-file removal checks passed again.

In the saved five-case comparison, the fixed workflow passed 5/5 cases and the
bounded agent passed 4/5. The failed agent run acknowledged missing costs but
computed net sales instead and returned completed status. This is a task
substitution failure, not an SQL-execution or access-control failure. Main
regional results and distinct-order counts were correct for both approaches.
Both main explanations were reviewed for values, dates, currency, completed
orders, line discounts, and missing regions; these matched the returned data.
The agent's ambiguity response confusingly lists top-N under time-window
choices, and the fixed refusal offers future deletion-script drafting. These
wording issues illustrate why passing status/result checks is insufficient to
establish explanation quality or policy alignment.

The MCP run discovered revenue_growth on its separate local server, received
arguments previous=1200000 and current=1500000 from the live model, returned
25.0, and produced the final answer "25% growth (denominator: $1,200,000)."
The server rejected a zero denominator. Both notebooks retain outputs and have
no error output cells. The deck was rendered and visually reviewed; the local
GitHub Pages source includes the lecture PDF, an original loop diagram with a
description, and separate links to both notebooks. Publishing awaits the normal
repository commit/push workflow.
