# Lecture 7 instructor notes

## Teaching arc

Start from the deployment decision and work backward to constructs,
instruments, observations, uncertainty, and claims. This keeps students from
treating an available benchmark or LLM judge as the definition of success.
Then move through the three ARIA testing levels: repeatable model tests,
adversarial red teaming, and realistic field testing. Close by validating the
evaluator and synthesizing evidence for a go, conditional-go, no-go, or
monitoring decision.

## Slide 8 notation

The symbol $\mathbb{1}(\hat y_i=y_i)$ is an indicator function. It equals 1
when the model's prediction on case $i$ is correct and 0 otherwise. The sum
therefore counts correct predictions, and division by $n$ gives empirical
accuracy. It is not an identity matrix. The displayed standard error is the
usual plug-in approximation for independent Bernoulli cases; dependence or
complex sampling calls for an appropriate paired, clustered, or bootstrap
analysis.

## Notebook discussion points

The benchmark is deliberately small. Its 100% live-run accuracy has a wide
Wilson interval and cannot support a production claim. The embedding example
also uses transparent prototypes; ask students how labels, thresholds, model
versions, and domain shift could invalidate it.

The LLM judge was perfectly repeatable across two runs in the saved execution
but agreed exactly with the small human reference ratings only 70% of the time.
This is a useful distinction between reliability and validity. The human
ratings are themselves only teaching references, not an authoritative gold
standard.

The red-team canary did not leak in the saved run, but the counterfactual
customer-support labels differed despite identical operational facts. Treat
that difference as a triage signal to reproduce and investigate, not as proof
of discrimination. A zero canary-leak rate over five attacks is likewise only
bounded evidence under the tested conditions.

## Facilitation cautions

Red teaming must be authorized, scoped, contained, and documented. Use only
synthetic secrets and fictional scenarios in class. Field studies involving
people may require institutional human-subjects review, privacy safeguards,
accessible participation, appropriate compensation, and a debriefing plan.

## Measurement trees

Do not assume that students will recognize *measurement tree* as a standard AI
evaluation term. The phrase appears in some measurement-science, systems, and
improvement contexts, but it is not used consistently and is also used for
unrelated technical concepts. Introduce the diagram as a simple evidence map:
observed indicators at the leaves, constructs in the middle, and a
decision-level claim at the root.

A small tree can make disagreement legible when sibling leaves retain their
separate values and conflicting branches are visibly marked. It should not
suggest that disagreement disappears through averaging. Pair the tree with a
plain-language legend and, if space permits, label it ``one way to organize
evidence'' rather than presenting it as a universally recognized formalism.

