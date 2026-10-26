# Lecture 3 instructor notes

## Through-line

Use the complaint-triage example to distinguish an LLM's generated text from an
application decision. The recurring question is: what evidence and controls are
needed before a generated value can influence an operational action?

## Demonstration sequence

1. Run the plain request and ask students which fields besides visible text an
   application needs to inspect.
2. Compare the two operating configurations. Treat the observed latency and
   usage as a small experiment, not as a general claim about all models.
3. Stream the acknowledgement and point to each displayed text delta: the API
   makes these response fragments available before the complete answer exists.
   Then explain why partially streamed JSON should not be consumed as a
   decision.
4. Contrast valid JSON with a schema-valid object and a business-valid object.
5. Ask why escalation is a positive, typed outcome rather than a model failure.
6. Run the three labeled cases. Emphasize that schema success does not prove a
   correct category or decision; carry the evaluation discussion into Lecture 7.

## Tool-use bridge

A useful first tool is a read-only lookup-recent-charges operation. Its
arguments can include an authenticated account reference plus a bounded date
range; its result can return charge identifiers, amounts, timestamps, and
statuses. The application, not the model, performs authorization and executes
the lookup. The model can then compare the complaint with returned records and
produce a typed recommendation. Keep refund execution out of this example:
verification is the teaching goal, and any financial action needs separate
authorization and approval controls.

Distinguish invalid JSON syntax from schema-invalid data. For example, a
negative refund amount is valid JSON, but it should fail a nonnegative amount
rule during Pydantic or JSON Schema validation. A validation error must stop
the application before the lookup function is called.

## Important cautions

- The example's retry decorator retries only transient connection, rate-limit,
  and server errors. It does not retry a refusal, incomplete output, schema
  failure, or business-rule failure; those need different application paths.
- Do not put production customer data or API keys in a notebook committed to a
  repository.
- A schema controls representational form, not truth, authorization, or policy
  compliance.
- The refund recommendation in the notebook never executes a refund. A real
  system needs identity checks, authorization, policy controls, logging, and an
  approval path.
- Treat model ``confidence'' or a score as uncalibrated unless it has been
  evaluated against labeled outcomes for the intended decision.

## Decisions API clarification

For a bounded decision with named choices and a returned confidence, use the
Decisions API shape:

    decision = client.decisions.create(
        model="gpt-6-luna",
        input=record_or_policy_text,
        questions=[{
            "type": "choice",
            "name": "next_step",
            "instructions": "Select the next step under the policy.",
            "choices": [
                {"value": "refund", "description": "Recommend a refund"},
                {"value": "close", "description": "Close without further action"},
                {"value": "escalate", "description": "Request human review"},
            ],
        }],
    )

This is preferable to a Responses API JSON-schema request when the teaching
goal is a bounded choice and its confidence. The response contains a typed
choice answer and confidence. Keep the local policy and authorization checks:
the model's choice does not itself authorize a refund. The official
[Decisions API guide](https://developers.openai.com/api/docs/guides/decisions)
documents this method, choice questions, and gpt-6-luna.

For a choice answer, do not assume that confidence equals the probability of
the selected option. The Decisions API documents the option probability
distribution and confidence as separate returned fields; its own illustrative
choice response shows 0.95 probability for the selected option and 0.93
confidence. Use labeled cases to determine whether either field is useful for
a particular threshold or review policy.

Abstention should be an explicit allowed Decisions API choice when the model
can recognize that it needs more evidence. It is distinct from an independent,
deterministic application guardrail: the application may override any model
choice and require review because of missing records, conflicting evidence, or
authorization policy.

Part 11 evaluates the same Decisions API pattern as Part 9. It records whether
the returned choice and probability distribution have the expected shape,
whether a deterministic local rule permits that choice, and whether it matches
the labeled action. These are different checks and should be discussed
separately.
