# Instructor notes: Lecture 2

## Few-shot examples and the live request

In a few-shot prompt, demonstrated input--output pairs belong to the examples. The final, live request should be visually distinct. An empty `## Output` heading can signal a response slot, but students may read it as part of the request or as text the model should reproduce. Prefer stating the required response format before the live request (for example, “Return only `billing` or `access`”), then end with the live request itself.

## Zero-shot prompting and criteria

Zero-shot means that a task is attempted without input--output demonstrations. It does not mean that every decision criterion is absent: a direct request can still state a label definition, response format, or rule. The relevant distinction is whether demonstrations are necessary for the task.

## Where to teach reasoning procedures

The course outline places the substantive treatment in Lecture 1, which explicitly covers reasoning models and inference-time reasoning. Lecture 2 should retain only the practical prompt-development distinction: a reasoning procedure is a staged request with intermediate checks, selected and evaluated like other prompting patterns. Return to the topic in Lecture 6 for tool-using and agentic procedures such as plan--act--observe loops. This division separates model- and inference-level mechanisms (Lecture 1), prompt design (Lecture 2), and operational orchestration (Lecture 6).

## Chain-of-thought versus broader reasoning procedures

For Lecture 2, use the more precise term *chain-of-thought prompting* rather than the broader “reasoning procedure.” Chain-of-thought is a prompt-side pattern that elicits intermediate text for a task. Broader reasoning procedures can also include hidden model reasoning, test-time search, self-consistency, verifiers, and tool-using agent loops; these are not merely prompt formats. Lecture 1 should cover inference-time reasoning and search, and Lecture 6 should cover tool-mediated procedures. When teaching chain-of-thought, emphasize that a visible trace is not proof or a causal explanation; assess the final answer with independent checks.

Chain-of-thought has both zero-shot and few-shot forms. The zero-shot form adds a request such as “Think step by step” to a task. The few-shot form provides demonstrations containing an input, intermediate reasoning, and a final answer, then presents a new input. The original chain-of-thought work used few-shot reasoning demonstrations; zero-shot chain-of-thought is a useful contrasting pattern. Slide 8 currently illustrates the zero-shot form.

## Instruction tuning and its risks

Define instruction tuning as supervised fine-tuning on instruction--response examples intended to improve instruction-following behavior. It is worth pairing this definition with a caution: fine-tuning can degrade general capabilities through catastrophic forgetting or overfitting, and it can regress safety or alignment behavior when the training data, objective, or evaluation coverage is inadequate. Present fine-tuning as a measurable intervention that needs held-out capability and safety evaluation, not as a routine replacement for prompt development.

## TikZ colors

TikZ inherits `xcolor` support, so there is no fixed practical limit on the number of colors. The deck can use named colors, tints and mixes such as `blue!15`, or custom colors defined with `\definecolor` in RGB, HTML, CMYK, or other supported color models. Prefer a small, consistent semantic palette for a single diagram; introduce a custom color only when it clarifies a distinct role.

## Reference ordering

Lecture 2 divides its bibliography into three explicit frames for legibility. Within each frame, `biblatex` sorts entries alphabetically by the first author or organization, not chronologically. The grouping is a layout choice rather than a conceptual sequence.

The current groups do not express a clean topical taxonomy. The first is primarily foundational and prompt-method research, the second primarily instructional, platform, and security sources, and the third contains later-added research and Codex material. If a semantic organization is desired, regroup the frames explicitly rather than inferring meaning from their present placement.

