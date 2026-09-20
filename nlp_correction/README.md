# NLP Correction Module (`nlp_correction/`)

Owner: Eyob Nebyou

Post-processing module that reduces recognition errors coming out of the
recognition model (`../ml/`), using Amharic-specific language patterns —
e.g. a character/word-level language model or dictionary-based
edit-distance correction.

## Folder layout

```
nlp_correction/
├── data/     Amharic lexicon / language-model resources (gitignored)
└── src/      Correction logic source code
```

## Dependency on `ml/`

This module's design depends on the error analysis produced in `ml/`
(objective 5 in the proposal — identifying common recognition errors such as
character substitutions, deletions, insertions, spacing errors, and visually
similar character confusions). Coordinate with Hallelujah on error-analysis
output format before finalizing the correction approach.

## Setup

```bash
cd nlp_correction
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Status

Scaffold only — no correction logic has been written yet.
