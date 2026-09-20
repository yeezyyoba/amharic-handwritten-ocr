# Recognition Model (`ml/`)

Owner: Hallelujah Ezra

Handwritten Amharic text recognition model. Primary architecture is a
CRNN+CTC (CNN feature extractor + BiLSTM + Connectionist Temporal
Classification). A fine-tuned Transformer-based model (TrOCR) will be
investigated as a secondary comparison.

## Folder layout

```
ml/
├── data/          Raw and processed dataset (gitignored — see below)
├── notebooks/     Exploration, experiments, error analysis
├── src/           Training/eval source code
└── models/        Trained model weights (gitignored — large binary files)
```

## Dataset

This project uses the [Fidel dataset](https://huggingface.co/datasets/upanzi/fidel-dataset) —
a large-scale sentence-level handwritten Amharic OCR dataset. It is not
committed to this repository. Download instructions will be added here once
access is confirmed.

Do not commit dataset files or trained model weights — both are excluded via
`.gitignore`. Use cloud storage, a release artifact, or Git LFS if the team
needs to share trained weights.

## Setup

```bash
cd ml
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Evaluation

Recognition performance is evaluated using:
- **Character Error Rate (CER)**
- **Word Error Rate (WER)**

Error analysis (character substitutions, deletions, insertions, spacing
errors, visually similar character confusions) feeds directly into the
NLP correction module's design — see `../nlp_correction/README.md`.

## Status

Scaffold only — no training code has been written yet.
