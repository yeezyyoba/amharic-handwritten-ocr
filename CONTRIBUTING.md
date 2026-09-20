# Contributing

## Workflow

1. Create a branch off `main` for your work (e.g. `hallelujah/dataset-prep`,
   `eyob/correction-baseline`, `leawi/capture-screen`).
2. Commit within your own module folder (`ml/`, `nlp_correction/`,
   `backend/`, or `mobile/`) unless the change is cross-cutting.
3. Open a pull request into `main` for review before merging.

## Do not commit

- Datasets (`ml/data/`, `nlp_correction/data/`) — see `ml/README.md` for
  where to get the Fidel dataset.
- Trained model weights (`ml/models/`) — share via cloud storage or a
  release artifact instead.
- `node_modules/`, Python virtual environments, `.env` files.

These are already covered by `.gitignore`, but double-check before pushing
large files.

## Cross-team dependencies

- `nlp_correction/` depends on error-analysis output from `ml/` — coordinate
  on the output format before finalizing correction logic.
- `backend/` depends on both `ml/` and `nlp_correction/` having a working
  interface before it can wire up the `/recognize` endpoint.
- `mobile/` depends on `backend/`'s API contract — check
  `backend/README.md` for the current (draft) request/response shape.
