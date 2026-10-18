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

## Notebook and GPU execution

- `model.summary()` reports the layer shapes and the parameter counts above; the following training loop reports each epoch and plots loss.
- TensorFlow uses a GPU automatically when it is visible to the selected Python environment. The project’s `tensorflow[and-cuda]` dependency and `scripts/configure_tensorflow_gpu.sh` make the required CUDA libraries discoverable for the project virtual environment.
- In VS Code, select `.venv/bin/python`, run the configuration script once, and reload the window/kernel so the generated GPU library-path environment is applied. CPU execution remains a supported fallback.
