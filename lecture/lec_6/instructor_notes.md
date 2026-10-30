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

Slide 4 labels the first transition "increased complexity" because connecting
external operations adds integration and execution controls. The second is
"increased autonomy" because the model gains discretion over the next step.
More external operations alone do not imply more model autonomy; a fixed
workflow can use many tools while retaining predefined control flow.
The slide's progression and design guidance adapt Anthropic's (2024)
*Building effective agents*, credited in a linked source line at the bottom
of the frame rather than a detached citation in the right column.

A tool implements an operation. A fixed workflow chooses the sequence in code;
its model may still choose a SQL statement or a typed stop decision. In an
agent, the model chooses some next steps based on feedback, while the host
retains tool permissions and limits. Tool calling alone does not imply a
general autonomous agent. A framework is optional: the short loop makes the
control flow and its stop conditions inspectable.

Slide 2 explicitly defines an agent as a software component that uses an LLM
to choose actions or next steps toward a goal, within application-defined
limits. Slide 3 distinguishes model-directed control flow, and slide 11
illustrates implementation with a model/tool loop. "A code module with an LLM
call" is a useful implementation intuition, but it also describes fixed
summarization or extraction steps. An agent
can be implemented with model calls, context/state, permitted tools, and stop
rules. Modularity is a design choice, not the distinguishing property of an
agent. The model need not run as a separate process, and multiple calls can
belong to one agent.

## Why these business definitions?

"Grain" is common vocabulary in data modeling, data warehousing, and analytics,
though it is not an SQL keyword. "Row-level detail" is a more accessible
introductory phrase. On slide 7, it means the level of detail represented by one row. A
customers row represents one customer; an orders row represents one order;
an order_items row represents one line item. Joining orders to order_items
produces item-level rows, so an order with three items appears three times.
`COUNT(*)` then counts items, while `COUNT(DISTINCT order_id)` counts orders.
Sum line-item amounts for sales, but do not sum an order-level total repeated
on each item row. Establish the intended row meaning before joining and
aggregating.

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

Slide 8 continues slide 7's request: "Which regions had the highest net sales
last quarter?" Slide 7 supplies the schema, row meaning, and business rules;
slide 8 implements those rules in SQL and shows the reference result. Its
three-table join, completed-status filter, July--September 2026 date interval,
discount subtraction, and Unknown region group all correspond to that request.

`COALESCE` returns its first non-NULL argument. On slide 8,
`COALESCE(c.region, 'Unknown')` replaces a missing region with the label
Unknown, while `COALESCE(i.discount_cents, 0)` replaces a missing discount with
zero. Otherwise subtracting a NULL discount produces NULL, and SUM ignores
that line's NULL amount, understating sales. These replacements implement
explicit business definitions rather than universally appropriate defaults.
COALESCE does not replace zero or an empty string, since neither is SQL NULL.

## Does slide 5 specify a result contract?

Yes. Slide 5 now places the request schema beside an application-defined
`QueryResult` type: `QuerySuccess` requires `ok=True`, `columns`, `rows`,
`truncated`, and `latency_ms`; `QueryError` requires `ok=False` and `error`, with
optional latency because argument rejection can occur before execution.
The former `get_schema()` bullet has been removed to make room. The type sketch
omits imports of `TypedDict`, `Literal`, and `NotRequired` from `typing`.

`strict=True` constrains generated arguments, not returned tool results.
`TypedDict` documents the executor's dictionary shapes; it does not add runtime
validation. The notebook separately checks success/truncation before using
results and compares returned data against independent references.

## Why does a SELECT-prefix check not suffice?

On slide 15, `PRAGMA` is SQLite's special command for inspecting or changing
database and connection settings. `PRAGMA query_only=ON` enables query-only
mode on the connection, preventing ordinary data/schema writes. It configures
execution rather than retrieving business records as SELECT does. PRAGMAs
are SQLite-specific rather than portable standard SQL. This setting is one
layer alongside the read-only connection and default-deny authorizer; the
model cannot issue arbitrary PRAGMAs through the approved query tool.

The slide 15 title "Explicitly restrict what agents can do" means
that each tool should receive only the access it needs, and application/database
controls should enforce those restrictions. For example, a sales-reporting tool
can read approved sales tables but cannot modify records or read private tables.
The title expresses least privilege in plain language. Restrictions on the
agent are enforced through its permitted tools, application code, and connected
systems.

Slide 15's last bullet (the Lecture 6 code example allows only three sales
tables and named functions)
refers to `connection.set_authorizer(allow_approved_reads)` in the simplified
code. The callback's body is omitted from the slide. In `utils.py`, the actual
callback is named `authorize` and consults `ALLOWED_TABLES` (customers, orders,
order_items) and `ALLOWED_FUNCTIONS`, denying other operations by default.
The PRAGMA and read-only connection do not themselves enforce those allowlists.

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

Bounded loops are general agent-control mechanisms, not SQL-specific concepts.
They open the Orchestration and oversight section, before the orchestration
patterns, multi-agent handoffs, and permission controls. Loop limits explain
how orchestration repeats steps and stops execution. The tool-neutral repair
example converts an explicitly supplied date into the format required by a
lookup tool. The Text2SQL notebook applies the same mechanism to a deliberately
seeded missing-column error; the SQL example points to that application without
making loop control a SQL-specific topic.

On slide 12, the left-hand pseudocode does not explicitly convert a date.
`history += request_and_result(response, result)` returns tool feedback to the
conversation; the next `ask_model(history)` can use that feedback to request a
revised argument. The right-hand date-format example illustrates that possible
repair. It is not a date parser hidden in `dispatch_checked_request`, nor does
the pseudocode guarantee that the model will repair the error correctly.

Slide 6 shows the two halves of the handoff in top-aligned columns. The left
column calls `client.responses.create` with the question, policy, and tool
contracts, checks completion, and preserves the response output. The right
column records, dispatches, and returns requested tool results by `call_id`.
To connect slides 5 and 6, slide 5 assigns the `run_query` definition to `TOOLS`,
which slide 6 passes to the model. Slide 6 asks "How many orders are there?";
the illustrated request uses `SELECT COUNT(*) FROM orders`. Its dispatcher
returns the `QueryResult` shape defined on slide 5, including `rows=[[9]]` for
the synthetic fixture. The annotation documents that shape without implying
runtime type enforcement. These captions illustrate a possible model request,
not a guarantee of the model's exact SQL or a new recorded API run.
Repeat the model call with the updated history to obtain the next step or final
answer; the Orchestration and oversight section supplies the enclosing stop rules.
The execution order is left, right, then left again: request a model response,
execute any requested tools and append their results, then call the model with
that evidence. If the first response is already a final answer without tool
requests, the right-hand loop performs no tool execution.

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

In slide 9's diagram, the dashed box labeled "MCP host" surrounds clients A--D.
It represents the coordinating application, not another server or the model
alone. In the calculator example, the notebook/Python application is the host:
it calls the model, manages ClientSession, adapts tool contracts, and controls
dispatch. The diagram shows its client connections rather than all its internal
model-integration and authorization code.

Slide 9 connects the contracts and dispatch on slides 5--6 to MCP's standard
protocol. `tools/list` discovers names, descriptions, input schemas, and optional
output schemas; `tools/call` sends tool names and arguments; result messages
carry returned content and tool-error status. MCP standardizes how contracts
are described and exchanged, not the business semantics of every tool.
Output schemas are optional; do not imply that all MCP tools supply them.
The host still adapts the discovered definition to its model provider's tool
format, validates requests/results, and enforces permissions. MCP does not
choose the SQL or turn a model request into business authorization. This
distinction is supported by the linked 2025-11-25 Tools specification.

The official page's displayed title is `Tools`. The dated URL places it within
version 2025-11-25 of the MCP specification, but `Protocol Specification` is
not the page title or a section heading. The BibTeX entry therefore uses the
exact title `Tools` and records `Model Context Protocol specification, version
2025-11-25` as a note. The page directly supports the slide's claims about
`tools/list`, `tools/call`, results, errors, input schemas, and optional output
schemas. The diagram's transport labels instead use the separate official
`Transports` page linked in the slide source line.

The notebook is the host; its ClientSession connects to a server process.
`list_tools` discovers `revenue_growth` and the safe but irrelevant
`sort_numbers`; the host exposes only those two allowlisted contracts. The
model selects `revenue_growth`, and the host checks that illustrative routing
decision, validates its arguments, and sends `call_tool` over MCP. The server
computes; the host
returns the observation to the model. Direct OpenAI HTTP requests and local
MCP stdio messages are distinct connections. A locally spawned server is not
a remote hosted MCP endpoint.

The second tool makes model selection observable: with `tool_choice='required'`
and only `revenue_growth`, the model previously chose arguments but not a tool.
`sort_numbers` is deterministic, side-effect-free, and clearly irrelevant to a
revenue-growth question. The host explicitly allowlists both discovered tools,
validates the selected name and arguments, and asserts that this worked example
selects `revenue_growth`. One successful choice is an illustration, not evidence
of general routing reliability; broader claims require repeated held-out routing
cases.

In Python, `async` marks code that participates in cooperative asynchronous
execution; it does not by itself start a thread or make code run in parallel.
`async def calculator_demo()` creates a coroutine function. Calling it creates
a coroutine object, and `await` runs it while allowing the event loop to do
other work whenever the coroutine is waiting for MCP I/O. The two `async with`
blocks enter and exit asynchronous context managers so the stdio connection and
client session are initialized and cleaned up without blocking the event loop.
The synchronous OpenAI SDK calls use `await asyncio.to_thread(...)` so those
blocking HTTP calls run in a worker thread while the notebook's event loop
remains responsive. Jupyter already runs an event loop, which is why the final
cell can use top-level `await` and should not wrap the coroutine in
`asyncio.run()`.

The calculator's final `client.responses.create` call is the second request in
a Responses API function-calling exchange, not a simple one-shot generation.
Its `input` value is a list of typed conversation items, not a list of function
arguments. The list contains the original user message, every item from the
first response (`*request.output`, including the function request and any
reasoning metadata), and a `function_call_output` containing the calculator
result. The matching `call_id` tells the model which requested function call
produced that result. Because the notebook sets `store=False`, it replays these
items explicitly rather than relying on stored state through
`previous_response_id`. No tools are supplied to the second call, so this
fixed workflow asks the model to turn the returned evidence into the final
answer rather than request another action.

The server never receives the host API key. Its stdout is protocol-only, and
the stdio client context starts and stops it. The calculator validates finite,
nonnegative revenues with a positive previous value; the notebook also checks
that the server rejects zero previous revenue. Use the same currency/scale
for both arguments. The formula is 100 * (current - previous) / previous = 25%.

On slide 10, `1_200_000` and `1_500_000` use Python's optional underscore digit
separators. They are numeric literals equal to `1200000` and `1500000`, not
strings or special MCP syntax. The underscores group digits for readability
and do not change the arithmetic. JSON numbers do not permit these separators;
the Python client serializes the numeric values without underscores.

The locked MCP dependency uses the v1 Python SDK interface, constrained below
v2 for reproducibility. Slide 9's editable vector adaptation updates the
archived IBM diagram's HTTP+SSE labels to Streamable HTTP, following the MCP
Transports specification. MCP discovery does not authenticate a
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

Slide 19's closing comparison aligns with the notebook: both designs use the
same synthetic data, definitions, model setting, dispatcher, and database
permissions, while the evaluation reports correctness, tool calls, token use,
and latency. The separate seeded-error run demonstrates the bounded agent's
repair path and the fixed workflow's inability to repair, but it is not an
unseeded accuracy comparison. Treat "cost" as the broader design burden of
extra calls, usage, latency, and oversight; the notebook does not calculate a
currency-denominated API cost. Its saved run also shows why the closing
question is genuine rather than rhetorical: the agent repaired the seeded SQL
error but used more input tokens and failed one unavailable-metric case that
the fixed workflow handled correctly.

## Why does slide 17 say not to require hidden chain-of-thought?

The slide distinguishes an auditable execution trace from a model's private
token-by-token reasoning. Evaluation and incident review should rely on
observable evidence that the application can consistently retain: model
status and usage, tool requests, validated arguments, execution results and
errors, stop status, and the final answer. Those records show what operation
was requested, what actually ran, what evidence returned, and whether the
answer is supported.

Hidden chain-of-thought is not a dependable control or audit interface. It may
be unavailable, incomplete, post-hoc, or different across model providers; it
can also expose sensitive prompt or context data and produce large, difficult
to govern logs. Even when a rationale sounds convincing, it does not prove
that the requested action was authorized or that the returned result supports
the answer. Conversely, an application can diagnose the regional-sales error
from the SQL, filters, returned rows, and final explanation without inspecting
private reasoning.

This does not prohibit concise, user-facing explanations or an explicitly
requested decision summary. Such text should be treated as another observable
model output and checked against tool evidence, not as privileged access to the
model's internal reasoning. The teaching point is to design traces and tests
that remain useful without hidden chain-of-thought.

## Where does planning fit in the orchestration table?

Slide 14 uses "orchestrator" for the agent or component that delegates bounded
work to agents and combines their results. This is established terminology
for the orchestrator--worker pattern. It describes the coordinating role, not
additional authority to bypass tools' permissions or handoff limits.

The diagram's "Handoff contents" label describes the information each
handoff should carry: the assigned objective and expected output; relevant
schema, definitions, records, or prior tool results; and constraints such as
permitted tools/data, read-only access, and remaining call/time budgets.
For example, the query agent receives a regional-sales question, schema
and date/metric definitions, and read-only execution limits. The report
agent receives the reporting task, verified query results and definitions,
and instructions to avoid unsupported claims. Agents should receive the
context needed for their assignments; it is not automatically inherited merely
because an orchestrator delegated work. Application code enforces permissions
and budgets even when they are described in a handoff message.

Planning belongs in slide 13's table, in the "Planning and execution" row.
It proposes steps or subgoals; execution carries them out under application
controls. The example identifies the tables, joins, filters, and aggregation
needed before querying. A model-generated plan does not authorize actions
or establish that the task is complete.

Clarifying an ambiguous metric can be part of planning because it resolves the
task's requirements before steps are chosen. It is not a distinct routing
pattern by itself. The revised routing example sends sales-data questions to
SQL and policy questions to document retrieval. Sequencing follows a predefined
generate/validate/execute/summarize path; reflection revises SQL after a real
missing-column error. These patterns can overlap, but each example emphasizes
its primary purpose. Routing to document retrieval illustrates the pattern;
the Text2SQL notebook itself does not implement a policy-retrieval tool.

## Agent identity and basic security (slide 16)

Slide 16 replaces the previous injection/blocked-write material. That topic
already appears in Lecture 2 slide 16 and Lecture 4 slide 7; validation and
approval controls also appear in Lecture 3. The replacement adds agent identity
and accountability, building on slide 15's execution restrictions.

Separate the role label from a verifiable software identity. Keep a responsible
owner and initiating user/request, scope credentials to the task, use short
lifetimes, recheck each tool call, log actions, and support revocation. Delegated
work must not gain wider access. These are design recommendations from Booth,
Fisher, Galluzzo, and Clancy's NIST blog (2026-10-27), not a claim that a new
mandatory standard has been issued.

The policy sketch uses fictional identifiers: sales-query-01 can read sales,
while sales-report-01 receives verified results without database access.
The ten-minute expiration is an illustrative choice, not a prescribed value.
Identity strings alone provide no authentication. A trusted credential and
its verification must bind the request to the identity; user_42 must come from
verified application context, not a model-supplied claim. An owner need not be
a human user issuing the current task; it can be the responsible team.

The slide is deployment guidance, not functionality added to the notebook.
The notebook has database controls and traces but does not provision separate
agent identities, credentials, or a multi-agent authorization service. A local
agent module does not inherently require its own OS process or API key.
Enforce logical-agent permissions through trusted application code or a broker
when multiple modules share a runtime.

Keep secrets out of prompts and handoffs; handoffs can name allowed scopes
without carrying raw credentials. MCP's Security Best Practices explains why
servers must validate intended tokens rather than blindly passing them to
other services. Credential lifecycle and permissions belong in connected
systems, not solely in model instructions. Retain human approval for
consequential actions as a short reminder; Lecture 6 implements no write or
approval service.

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

The original IBM architecture PNG is retained from `HR_AI_Exec_Ed.zip`'s
`img/model-context-protocol.png` for provenance. Slide 9 uses an editable
`asset/model-context-protocol.svg` adaptation with a vector PDF for pdfLaTeX.
It preserves the host/client/server layout and updates the transport labels,
crediting IBM and linking the official MCP Transports specification.
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

The updated MCP run discovered `revenue_growth` and `sort_numbers` on its
separate local server. Given a revenue-growth question, the live model selected
`revenue_growth`, supplied previous=1200000 and current=1500000, and received
25.0. The final answer was "25% growth, based on a denominator of $1,200,000."
The host includes an assertion that would reject the irrelevant selection, and
the server rejected a zero denominator. Both notebooks retain outputs and have
no error output cells. The deck was rendered and visually reviewed; the local
GitHub Pages source includes the lecture PDF, an original loop diagram with a
description, and separate links to both notebooks. Publishing awaits the normal
repository commit/push workflow.
