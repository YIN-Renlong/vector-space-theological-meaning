# CTSB v3.5-alpha Generated 100-Concept Benchmark

## Evidential status

This directory contains a generated, unreviewed, and non-evidential development benchmark.

It must not be presented as a final CTSB benchmark or as validated theological evidence.

## Generated tables

The `generated_100/` directory contains:

- `comparisons.csv` — 100 audit definitions;
- `references.csv` — 600 generated reference anchors;
- `queries.csv` — 1,624 controlled query inputs;
- `validation.csv` — 808 generated development-validation passages.

The five CTSB v3.4 prototype audits are retained:

- death versus biological description;
- grief versus psychological bereavement;
- euthanasia versus a permissive assisted-dying register;
- grace versus elegance and social charm;
- judgment after death versus generic religious afterlife judgment.

## Important restrictions

The reference statements are not quotations or verified paraphrases.

Candidate source titles identify possible future source classes only. Exact source support, exact locations, wording fidelity, theological accuracy, and disciplinary accuracy remain unverified.

The validation passages are not genuinely independent held-out validation.

## Commands

Regenerate the tables:

    .venv/bin/python scripts/ctsb_v3_5_alpha.py write-data --force

Validate the generated structure:

    .venv/bin/python scripts/ctsb_v3_5_alpha.py validate

Run the deterministic mock analysis:

    .venv/bin/python scripts/ctsb_v3_5_alpha.py run --backend mock

Run the automated alpha tests:

    .venv/bin/python tests/test_ctsb_v3_5_alpha.py

Azure should be run only after safeguards, tests, documentation, and Git state have been checked.

Generated vectors, caches, and run outputs remain local under `outputs/v3_5_alpha/` and must not be committed.
