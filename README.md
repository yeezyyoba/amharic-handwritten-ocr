# Handwritten Amharic Text Recognition Mobile Application

A mobile application that recognizes handwritten Amharic text from a captured
or uploaded image and converts it into an editable digital document. A
recognition model converts the image to text, an NLP-based correction module
reduces recognition errors, and the result is shown in an editable interface
for the user to review, correct, and export.

Senior project — Department of Computer Science, College of Natural and
Computational Sciences, Addis Ababa University.

Full proposal: [`docs/proposal.md`](docs/proposal.md)
System architecture: [`docs/architecture.md`](docs/architecture.md)

## Team

| Name | ID | Role |
|---|---|---|
| Hallelujah Ezra | UGR/4392/16 | Computer vision & recognition model |
| Eyob Nebyou | UGR/5588/16 | NLP correction module |
| Leawi Taddesse | UGR/4913/16 | Mobile app & integration (assists on CV/NLP) |

Advisor: Mr. Surafiel Habib

## Project structure

```
amharic-ocr-app/
├── docs/              Proposal, architecture notes
├── ml/                Recognition model (CRNN+CTC, TrOCR comparison)
├── nlp_correction/    Post-processing correction module
├── backend/           FastAPI service that hosts the recognition + correction pipeline
└── mobile/            React Native mobile application
```

Each subfolder has its own `README.md` with setup instructions for that
component.

## Tech stack

- **Mobile app:** React Native
- **Backend:** Python, FastAPI
- **Recognition model:** Python, PyTorch (CRNN+CTC primary, TrOCR via
  Hugging Face Transformers as a comparison)
- **NLP correction:** Python (Amharic-specific correction logic)
- **Dataset:** [Fidel](https://huggingface.co/datasets/upanzi/fidel-dataset) —
  handwritten Amharic OCR dataset
- **Version control:** Git / GitHub

## Getting started

Each component is developed and run independently during this stage of the
project. See:

- [`ml/README.md`](ml/README.md) — recognition model setup
- [`nlp_correction/README.md`](nlp_correction/README.md) — correction module setup
- [`backend/README.md`](backend/README.md) — backend service setup
- [`mobile/README.md`](mobile/README.md) — mobile app setup

## Status

This repository currently contains the project scaffold only — folder
structure, dependency files, and documentation. Implementation begins once
the proposal is approved.
