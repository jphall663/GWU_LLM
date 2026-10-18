# Lecture 1: Next-token MLP primer

`next_word_primer.ipynb` and the slides built from `lecture_1.tex` present the
same small next-token model: a four-token context window, two-dimensional
token embeddings, four hidden units, and six output probabilities.

Concise teaching and implementation notes are in [instructor_notes.md](instructor_notes.md).

## Reproducible Python environment

From the repository root, install the locked Python 3.13 environment:

```bash
uv sync --locked
```

Run the notebook without GPU acceleration:

```bash
uv run jupyter lab lecture/lec_1/next_word_primer.ipynb
```

The notebook uses CPU automatically when no compatible GPU is available.

## Optional NVIDIA GPU acceleration

This configuration applies to Linux systems with an NVIDIA GPU and a working
NVIDIA driver. Confirm driver access first:

```bash
nvidia-smi
```

The lockfile includes TensorFlow's `and-cuda` extra. After each fresh `uv sync`
or virtual-environment recreation, configure TensorFlow's CUDA library paths:

```bash
./scripts/configure_tensorflow_gpu.sh
```

The script creates only project-local links inside `.venv` and a local,
ignored VS Code environment file. It finishes by printing TensorFlow's detected
GPU devices. If it reports no GPU, the notebook remains usable on CPU.

### VS Code

1. Run `./scripts/configure_tensorflow_gpu.sh` from the repository root.
2. Reload the VS Code window after the script finishes.
3. In the notebook kernel picker, select the project interpreter:
   `.venv/bin/python`.
4. Restart the notebook kernel and run the first cell. It prints the Keras
   backend and detected device names.

The tracked workspace settings point VS Code at the generated environment file;
the file itself is machine-specific and intentionally not committed.
