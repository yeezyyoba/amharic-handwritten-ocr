# Handwritten Amharic Text Recognition Mobile Application

A mobile application that recognizes handwritten Amharic text from a captured
or uploaded image and converts it into corrected, editable digital text. A
recognition model (CRNN+CTC, with a fine-tuned TrOCR model as a comparison)
converts the image to text, an NLP-based correction module reduces recognition
errors, and the result is shown in an editable interface for the user to
review, correct, save and export.

Final Year Project, BSc in Computer Science, Department of Computer Science,
College of Natural and Computational Sciences, Addis Ababa University (2026/27).
A companion technical report for CoSc4511 (Technical Report Writing) compares
CRNN+CTC and TrOCR on handwritten Amharic; see `docs/technical-report/`.

## Team

| Name | ID | Section | Primary work package |
|---|---|---|---|
| Eyob Nebyou | UGR/5588/16 | 1 | NLP correction module |
| Hallelujah Ezra | UGR/4392/16 | 1 | Computer vision and recognition model |
| Leawi Tadesse | UGR/4319/16 | 2 | Mobile application and integration |
| Maryamawit Lemma | UGR/6995/16 | 2 | Quality assuring and app integration |

Advisor: Mr. Surafiel Habib

Every member must hold primary responsibility for at least one major work
package (guideline Section 14.2). Fill in the last row and keep it in sync with
`docs/compliance/contribution-statements/`.

## Project status

| Phase (FYP I, Semester I) | Report chapter | Status |
|---|---|---|
| 1. Proposal | Chapter 1 (Introduction) | Approved |
| 2. Literature review | Chapter 2 | In progress |
| 3. Methodology | Chapter 3 | Not started |
| 4. Requirements analysis (and design) | Chapter 4 | Not started |

Early experimental work also exists: a first CRNN+CTC model trained on Fidel
(best validation CER 0.165, epoch 13) and a synthetic-error NLP correction
baseline. See `ml/results/README.md`.

## Repository structure

```
amharic-handwritten-ocr/
├── docs/                          All project documents (see docs/README.md)
│   ├── 00-guidelines/             Department FYP guideline (Oct 2026, v2.0)
│   ├── 01-proposal/               Approved proposals and earlier draft
│   ├── 02-literature-review/      Reading matrix, comparison table, Chapter 2 draft
│   ├── 03-methodology/            Chapter 3 draft
│   ├── 04-requirements-and-design/ Fact finding, SRS, architecture, diagrams, Chapter 4
│   ├── fyp1-document/             Front matter, Chapter 1, assembled FYP I document
│   ├── project-management/        Logbook, risk register, traceability, minutes, changes
│   ├── compliance/                AI-use disclosure, ethical screening, contribution statements
│   └── technical-report/          CoSc4511 technical report (CRNN+CTC vs TrOCR)
├── ml/                            Recognition model and NLP correction (Python, PyTorch)
├── backend/                       FastAPI service hosting recognition + correction
└── mobile/                        Flutter mobile application
```

Each code folder has its own `README.md` with setup instructions.

## Tech stack (as approved in the proposal)

- **Mobile app:** Flutter (Dart)
- **Backend:** Python, FastAPI
- **Recognition:** Python, PyTorch (CRNN+CTC); Hugging Face Transformers (TrOCR comparison)
- **NLP correction:** Python (dictionary / edit-distance and language-model based correction)
- **Database:** PostgreSQL (images stored as files, paths in the database)
- **Datasets:** [Fidel](https://huggingface.co/datasets/upanzi/fidel-dataset) and
  AHL-D 29K (Amharic Handwritten Line Dataset)
- **Version control:** Git / GitHub

## Getting started

- [`ml/README.md`](ml/README.md): recognition model and NLP correction
- [`backend/README.md`](backend/README.md): backend service
- [`mobile/README.md`](mobile/README.md): mobile app

Datasets and trained weights are not committed (see `.gitignore`).
