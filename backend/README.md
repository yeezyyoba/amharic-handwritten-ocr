# Backend (`backend/`)

Owner: shared (integration led by Leawi)

FastAPI service that hosts the recognition model (`../ml/`) and the NLP
correction module (`../nlp_correction/`) as a remote API consumed by the
mobile app (`../mobile/`).

## Folder layout

```
backend/
├── app/
│   ├── routes/     API endpoint definitions
│   ├── services/   Calls into ml/ and nlp_correction/
│   └── models/     Request/response schemas
└── tests/          Backend tests
```

## Planned API (draft — will change once the recognition model's I/O is finalized)

`POST /recognize`
- **Request:** image file (multipart/form-data)
- **Response:** JSON — recognized-and-corrected text, plus optionally the
  raw (pre-correction) text for debugging/error analysis

This contract is not final. Update this section once `ml/` and
`nlp_correction/` have working interfaces.

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Status

Scaffold only — no endpoints have been implemented yet.
