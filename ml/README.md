# Machine Learning (`ml/`)

The machine learning component of the Amharic Handwritten OCR project.

The ML pipeline consists of two connected research stages:

1. **Handwritten text recognition** using a CRNN + CTC architecture.
2. **NLP-based post-processing** to correct recognition errors produced by the OCR model.

## Folder Structure

```text
ml/
├── data/
│   ├── raw/            Raw resources and lexicons
│   ├── processed/      Processed datasets
│   └── predictions/    OCR prediction outputs
├── models/              Trained model weights
├── notebooks/            Training, experiments, and analysis
├── results/
│   ├── metrics/         Training and evaluation metrics
│   └── predictions/     Sample and analysis outputs
├── src/                  CRNN training and evaluation code
├── requirements.txt
└── README.md
```

## OCR Recognition Model

The primary recognition architecture is a **CRNN + CTC** model consisting of:

* CNN-based visual feature extraction
* Bidirectional LSTM sequence modeling
* Connectionist Temporal Classification (CTC) decoding

A fine-tuned Transformer-based OCR model such as TrOCR may be investigated as a secondary comparison.

### Current Evaluation

The CRNN is evaluated using:

* Character Error Rate (CER)
* Word Error Rate (WER)
* Exact sentence accuracy

The validation split is writer-disjoint to evaluate generalization to handwriting from unseen writers.

## NLP Correction

The NLP correction work is implemented as a notebook-based research workflow.

The pipeline is:

```text
OCR prediction
      ↓
Text normalization
      ↓
Tokenization
      ↓
Candidate generation
      ↓
Dictionary / edit-distance correction
      ↓
OCR confusion-aware ranking
      ↓
Corrected text
      ↓
CER / WER evaluation
```

The NLP experiments use Amharic lexical resources and investigate character-level and word-level OCR errors.

The correction approach will be informed by empirical error analysis from the recognition model rather than relying only on manually defined confusion rules.

## Notebooks

### `02_nlp_correction_baseline.ipynb`

Initial NLP correction experiments using synthetic OCR errors and an Amharic wordlist.

This notebook establishes the baseline correction approach before applying it to real OCR predictions.

### `crnn_extended.py`

Extended CRNN training and evaluation workflow.

This script performs model training, validation, checkpointing, and evaluation.

## Dataset

The project uses the **Fidel handwritten Amharic OCR dataset**.

The dataset itself is not committed to the repository. Raw and processed datasets should remain excluded through `.gitignore`.

## Setup

```bash
cd ml

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Evaluation

Recognition and correction performance are evaluated using:

* **CER (Character Error Rate)** — lower is better
* **WER (Word Error Rate)** — lower is better
* **Exact sentence accuracy** — percentage of samples with no recognition errors

NLP correction will be evaluated against the original OCR output to determine whether post-processing reduces errors without introducing additional errors.

## Research Workflow

The intended workflow is:

```text
Fidel Dataset
     ↓
CRNN Training
     ↓
OCR Predictions
     ↓
Character-level Error Analysis
     ↓
NLP Correction
     ↓
Corrected Predictions
     ↓
CER / WER Comparison
```

The NLP correction experiments should use training-derived resources where appropriate and must avoid using validation ground-truth text to learn correction mappings, preventing evaluation leakage.

## Status

The CRNN recognition pipeline has been implemented and evaluated.

The NLP correction component is currently being developed as a notebook-based research experiment using the CRNN predictions and empirical OCR error statistics.

