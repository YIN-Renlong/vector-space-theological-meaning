# CTSB v3.5-alpha Generated 100-Concept Benchmark

## Status — completed development milestone

CTSB v3.5-alpha is complete as a generated, unreviewed, and non-evidential development experiment.

It demonstrated 100-concept data handling, mock analysis, Azure integration, reference-level scoring, component decomposition, leave-one-reference-out analysis, paraphrase sensitivity, statistical summaries, hashing, and manifest generation.

It is not a final or independently validated benchmark.

## Tracked generated tables

The `generated_100/` directory contains:

- `comparisons.csv` — 100 audit definitions;
- `references.csv` — 600 generated reference anchors;
- `queries.csv` — 1,624 controlled queries;
- `validation.csv` — 808 generated development-validation passages.

The five CTSB v3.4 audits are retained:

- death versus biological description;
- grief versus psychological bereavement;
- euthanasia versus permissive assisted dying;
- grace versus elegance and social charm;
- judgment after death versus generic religious judgment.

## Completed runs

A deterministic mock run and a successful Azure run were completed locally.

The Azure run:

- embedded 3,032 unique texts;
- used 48 API batches;
- returned `text-embedding-3-large`;
- returned 3,072-dimensional vectors;
- produced 1,624 query scores;
- produced 1,524 matched shifts;
- produced 14,592 query/validation-to-reference similarities;
- and passed numerical and hash checks.

Generated vectors, caches, run outputs, and reports remain local under `outputs/v3_5_alpha/` and are intentionally excluded from Git.

## Evidential restriction

The reference statements are:

- generated;
- unreviewed;
- not quotations;
- not verified paraphrases;
- and not verified source summaries.

Candidate source titles identify possible future source classes only.

The validation passages were generated from the same conceptual fields used for reference construction. Their perfect classification result is a pipeline diagnostic, not independent held-out validation.

The alpha results must not be presented as findings of theological attenuation, Catholic adequacy, model bias, or pastoral reliability.

## Main methodological lesson

The alpha demonstrated that a positive CAS shift can occur while Catholic-reference similarity declines.

Therefore:

> Positive relative movement must not be described as theological recovery unless component-level analysis confirms positive Catholic-reference gain.

## Next phase

The next planned phase is CTSB v3.5-beta.

Read:

- [`../../../docs/AI_HANDOFF_V3_5_BETA.md`](../../../docs/AI_HANDOFF_V3_5_BETA.md)
- [`../../../docs/CTSB_V3_5_BETA_PLAN.md`](../../../docs/CTSB_V3_5_BETA_PLAN.md)

Beta will focus on natural-language quality, construction-leakage reduction, separate validation authoring, label balance, calibration, and operationalisation of theological framing–content divergence.

## Commands

Validate the tracked alpha data:

    .venv/bin/python scripts/ctsb_v3_5_alpha.py validate

Run the alpha tests:

    .venv/bin/python tests/test_ctsb_v3_5_alpha.py

Regenerate the development tables:

    .venv/bin/python scripts/ctsb_v3_5_alpha.py write-data --force

No additional alpha Azure run is presently required.
