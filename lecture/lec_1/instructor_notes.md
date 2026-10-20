# Instructor notes: Lecture 1

## Context windows, vocabulary, and embeddings

- The example has a context-window length of \(L=4\): each prediction uses four token IDs (left-padded when the prefix is shorter).
- The vocabulary has six tokens, so the model learns one embedding per vocabulary item: \(\mathbf E\in\mathbb R^{6\times2}\). The four context positions do **not** limit the table to four embeddings.
- An embedding lookup gathers the rows indexed by the four input IDs. Thus a four-token context produces \(\mathbf E_{\mathbf x}\in\mathbb R^{4\times2}\), which is flattened to eight values. The table remains in memory; rows are not swapped in or out.
- The embedding table is learned by backpropagation. On an example, the input token rows receive direct updates; over the data, tokens appearing in contexts learn their own vectors.
- “Learned” describes how the table values are obtained; “lookup” describes selecting a learned row for a token ID. A useful phrasing is: “Each token ID looks up its learned embedding vector.”

## Layer shapes and parameter counts

The model flow is \((4,2)\rightarrow8\rightarrow4\rightarrow6\): four two-dimensional embedding vectors, eight flattened coordinates, four `tanh` hidden units, and six softmax probabilities. Each layer’s output must have the shape expected by the next layer’s input.

- Embedding table: \(6\times2=12\) parameters.
- Hidden layer: \(8\times4\) weights plus four biases, or \(36\) parameters.
- Output layer: \(4\times6\) weights plus six biases, or \(30\) parameters.
- Total: \(12+36+30=78\) trainable parameters.

## Objective function

Categorical cross-entropy is also called **multiclass log loss**. For a single example with correct target ID \(y\), the loss is \(-\log \hat p_y\): the negative log of the probability assigned to the observed next token. For example, if the correct token receives probability \(0.80\), the loss is \(-\log(0.80)\approx0.223\).

## Attention and self-attention

- **Attention** is the general mechanism in which queries use compatibility scores with keys to weight and combine values; the queries and the key--value pairs may come from different sequences or representations.
- **Self-attention** is the special case in which the queries, keys, and values are projections of the same sequence of tokens. The equation on slide 10 therefore depicts self-attention in its current transformer context.
- Slide 10 states: “In self-attention, queries, keys, and values are derived from the same sequence of tokens.”
- More precisely, at each token position, learned linear transformations map the input representation \(\mathbf{x}_i\) to a query, key, and value vector: \(\mathbf{q}_i=\mathbf{x}_i\mathbf{W}_Q\), \(\mathbf{k}_i=\mathbf{x}_i\mathbf{W}_K\), and \(\mathbf{v}_i=\mathbf{x}_i\mathbf{W}_V\). “Projection” is common shorthand, although these learned maps need not be projections in the strict mathematical sense.
- “Input token embedding” is precise only for the first transformer layer and only when the phrase includes positional information. Later layers transform contextualized hidden representations rather than the original token embeddings. For a layer-independent description, prefer “the representation at each token position”; when discussing the first layer specifically, “the position-enriched token embedding” is more exact.
- On slide 10, “attention weights” refers to the query-dependent coefficients produced by the row-wise softmax of \(QK^\top/\sqrt{d_k}\), not the learned parameter matrices \(W_Q\), \(W_K\), and \(W_V\). For each query, these coefficients determine how strongly each position's value vector contributes to the attention output.

## From the final hidden state to the next token

For an autoregressive language model, the final transformer block produces a contextualized hidden vector at each sequence position. The vector at the last position, \(\mathbf h_t\in\mathbb R^{d_{\text{model}}}\), usually has the same width as a token embedding, but it is not yet a next-token prediction.

An output linear map, often called the language-model head or unembedding layer, converts that hidden vector into vocabulary logits:

\[
\widetilde{\mathbf h}_t=\operatorname{LayerNorm}(\mathbf h_t),
\qquad
\mathbf z_t = \mathbf W_U\widetilde{\mathbf h}_t + \mathbf b_U,
\qquad
\mathbf z_t\in\mathbb R^{|V|}.
\]

Here \(\mathbf W_U\in\mathbb R^{|V|\times d_{\text{model}}}\). Its row \(\mathbf w_v^\top\) is the learned output vector for vocabulary item \(v\), so that token's logit is

\[
z_{t,v}=\mathbf w_v^\top\widetilde{\mathbf h}_t+b_v.
\]

The model therefore compares the current hidden state with one learned output direction per vocabulary item, computing all \(|V|\) scores in one matrix multiplication. A higher inner product gives that token a higher unnormalized score; the bias, when the architecture includes one, can shift the score independently of the hidden state. Final normalization is architecture-dependent but common, and some language-model heads omit the bias.

During training, next-token cross-entropy encourages the logit for the observed next token to rise relative to the other logits. Gradients jointly adjust the output vectors and the preceding transformer layers, teaching the network to place \(\widetilde{\mathbf h}_t\) in a region that scores the appropriate continuations highly.

In short, the model learns the output-head weights that map a final hidden state to one logit per vocabulary item. It does not learn the vocabulary membership at this stage: the tokenizer defines the vocabulary beforehand, and training learns how to score those fixed token IDs in context.

Softmax normalizes the logits into a probability distribution:

\[
p(x_{t+1}=v\mid x_{\le t})
=\frac{\exp(z_{t,v})}{\sum_{u\in V}\exp(z_{t,u})}.
\]

The vocabulary index chosen by greedy decoding or sampling is passed back through the tokenizer to obtain a token. During continued generation, that token ID is appended to the sequence and its embedding participates in the next forward pass. Temperature and other decoding controls modify the logits or candidate probabilities before selection; they do not change the learned hidden-state-to-vocabulary map.

For temperature-scaled sampling, \(p_v(T)=\operatorname{softmax}(z_v/T)\) with \(T>0\). A lower temperature magnifies logit differences, producing a sharper distribution with more probability on the highest-scoring tokens. A higher temperature compresses those differences, producing a flatter distribution and increasing the relative probability of lower-scoring tokens. Positive temperature scaling does not change the ordering of the logits, so it does not change the greedy argmax; it changes the probabilities used for sampling. As \(T\to0^+\), the distribution approaches an argmax choice, while very large \(T\) moves it toward a uniform distribution over the unfiltered vocabulary.

Thus, the final hidden state has length \(d_{\text{model}}\), while the next-token prediction vector has length \(|V|\). These lengths coincide only accidentally. Many models tie the output weights to the input embedding matrix. With an input embedding table \(\mathbf E\in\mathbb R^{|V|\times d_{\text{model}}}\), the tied map is \(\mathbf W_U=\mathbf E\). Under the alternative row-vector convention, the same calculation is written \(\mathbf z_t=\widetilde{\mathbf h}_t^\top\mathbf E^\top+\mathbf b_U\). Weight tying reuses parameters but does not make the vocabulary-sized prediction vector embedding-sized.

## Reasoning traces and inference-time compute

Slide 14 uses a linear user-prompt-to-reasoning-tokens-to-response diagram to represent a reasoning model spending additional inference-time computation before returning a user-visible response. The displayed reasoning tokens are an explanatory abstraction: do not confuse a trace with a causal explanation. A reported trace can be plausible or useful without faithfully exposing the model's internal causal process.

Slide 13 shows several candidate reasoning paths feeding a selected answer. This is a multi-candidate inference-time-compute pattern, such as best-of-\(N\), self-consistency, or verifier-guided selection. The selection mechanism need not be internal to the language model: it can be majority voting, a learned reward model, a separate verifier, a rule-based checker, or another external scoring procedure. The diagram does not identify which criterion is used. It is paired with the compute--quality curve to show that generating and evaluating candidates consumes additional inference-time resources and may exhibit diminishing returns.

Reasoning is not always equivalent to extra inference-time compute. A model can acquire reasoning capabilities during training and can sometimes answer within an ordinary fixed decoding budget. Inference-time scaling specifically means deliberately allocating more computation at inference, for example by generating a longer reasoning trace, sampling multiple candidates, invoking a verifier, revising an answer, or searching possible continuations. When a model emits additional reasoning tokens before its answer, those autoregressive decoding steps do consume additional inference-time compute relative to a shorter direct response.

The slides use a general-to-specific progression: generation, the broader set of inference-time scaling strategies, and then additional reasoning tokens as one strategy plus the warning that a trace is not a causal explanation.

## Overall summary

Slide 16 summarizes the lecture in a text-to-response progression. Use “tokenization and encoding” rather than treating an entire word as the basic unit: a tokenizer maps text to token IDs, and an embedding table maps those IDs to learned vectors. Embeddings can represent learned features and similarities, but should not be described as directly containing “logic.”

Within a transformer block, feed-forward networks operate independently at each token position, while self-attention is the main mechanism that mixes information across positions. In a causal language model, a position attends only to itself and earlier positions. Residual connections and normalization help preserve information and stabilize training. Stacking blocks increases representational capacity; it is more precise to say “transformer blocks” than “encoder/decoder blocks” because many contemporary LLMs are decoder-only.

Generation does not decode an embedding directly into a word. The output head maps the final hidden vector to vocabulary logits, softmax produces next-token probabilities, and a decoding rule selects or samples a token ID. The tokenizer renders that token as text, and autoregressive generation repeats the process. Inference-time scaling can allocate additional computation to longer reasoning, multiple candidates, search, or verification; this is more precise than saying that the transformer literally “thinks.” Alignment then refers to training and evaluation methods that steer model behavior toward instructions, preferences, and safety goals without guaranteeing truth or safety.

## Notebook and GPU execution

- `model.summary()` reports the layer shapes and the parameter counts above; the following training loop reports each epoch and plots loss.
- TensorFlow uses a GPU automatically when it is visible to the selected Python environment. The project’s `tensorflow[and-cuda]` dependency and `scripts/configure_tensorflow_gpu.sh` make the required CUDA libraries discoverable for the project virtual environment.
- In VS Code, select `.venv/bin/python`, run the configuration script once, and reload the window/kernel so the generated GPU library-path environment is applied. CPU execution remains a supported fallback.
