# System Architecture

## Overview

The system has three independently developed parts that come together through
a remote backend service:

```
┌─────────────────┐        image        ┌──────────────────┐
│                  │ ──────────────────► │                  │
│  Mobile App      │                     │  Backend (FastAPI)│
│  (React Native)  │ ◄────────────────── │                  │
│                  │   corrected text    └──────────────────┘
└─────────────────┘                              │   ▲
                                                  ▼   │
                                        ┌──────────────────┐
                                        │ Recognition Model │
                                        │ (CRNN+CTC / TrOCR)│
                                        └──────────────────┘
                                                  │
                                                  ▼
                                        ┌──────────────────┐
                                        │  NLP Correction   │
                                        │      Module        │
                                        └──────────────────┘
```

## Flow

1. **Capture/upload** — the user captures or uploads an image containing
   handwritten Amharic text in the mobile app.
2. **Send to backend** — the mobile app sends the image to the backend over
   HTTPS.
3. **Recognition** — the backend runs the image through the recognition model
   (CRNN+CTC primary, with a fine-tuned TrOCR model investigated as a
   comparison) and produces raw recognized text.
4. **Correction** — the raw output is passed through the NLP correction
   module, which reduces character-level and spacing errors using
   Amharic-specific language patterns.
5. **Response** — the corrected text is returned to the mobile app.
6. **Review & edit** — the user sees the corrected text in an editable
   interface, makes any final corrections, and saves or exports the result.

## Components

| Component | Responsibility | Owner |
|---|---|---|
| `ml/` | Dataset prep, model training, evaluation (CER/WER), error analysis | Hallelujah |
| `nlp_correction/` | Post-processing correction of recognition output | Eyob |
| `backend/` | Hosts recognition + correction pipeline as a remote API | Shared |
| `mobile/` | Capture/upload UI, editable text interface, export | Leawi |

## API (planned)

The backend will expose an endpoint to accept an image and return corrected
text. The exact request/response shape will be finalized once the recognition
model's output format is settled — see `backend/README.md` for the current
placeholder contract.

## Evaluation

The recognition component is evaluated using:
- **Character Error Rate (CER)**
- **Word Error Rate (WER)**

Common error types (substitutions, deletions, insertions, spacing errors,
visually similar character confusions) are analyzed to guide the correction
module's design.
