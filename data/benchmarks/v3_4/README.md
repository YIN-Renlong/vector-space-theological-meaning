# CTSB v3.4 Benchmark Construction Area

## Status

No final v3.4 benchmark has been frozen.

This directory is reserved for the redesigned, source-grounded benchmark.

## Planned benchmark components

### 1. Concept registry

Planned fields:

- benchmark version;
- concept ID;
- concept;
- theological locus;
- critical-context applicability;
- comparison-register type;
- theological relationship type;
- inclusion rationale;
- review status.

### 2. Catholic reference registry

Planned fields:

- concept ID;
- Catholic reference ID;
- natural-language reference text;
- authoritative source;
- source location;
- quotation or paraphrase status;
- reviewer decision;
- review notes;
- frozen status.

### 3. Comparison-register registry

Planned fields:

- concept ID;
- comparison reference ID;
- register name;
- register subtype;
- natural-language reference text;
- empirical or disciplinary source;
- reviewer decision;
- frozen status.

### 4. Query-condition registry

Potential conditions:

- bare/minimal;
- natural general use;
- natural ambiguity;
- critical/crisis context;
- label-free theological content;
- explicit Catholic context;
- integrative theological-proximate context.

Applicability must be declared before evaluation.

### 5. Held-out validation set

The validation texts must:

- remain separate from reference construction;
- use natural language;
- be independently labelled;
- include clear-register examples;
- include a separate integrative subset;
- avoid unnecessary lexical overlap with the references.

### 6. Descriptor-level output schema

Every query-to-reference comparison should retain:

- query ID;
- concept ID;
- query condition;
- query text;
- reference ID;
- original reference text;
- reference register;
- cosine similarity;
- within-concept rank;
- model metadata;
- timestamp;
- benchmark version.

## Freeze procedure

Before final evaluation:

1. complete source collection;
2. complete theological and linguistic review;
3. resolve reviewer disagreements;
4. freeze reference and query texts;
5. freeze held-out validation texts;
6. publish the statistical analysis plan;
7. tag the benchmark version;
8. only then run the final embedding audit.

No v3.4 result should be labelled final if the benchmark was revised after inspecting that result.

## Synthetic development prototype

The `prototype/` directory contains five illustrative audit units:

- death versus biological description;
- grief versus psychological bereavement;
- euthanasia versus a permissive assisted-dying register;
- grace versus elegance and social charm;
- judgment after death versus generic religious afterlife judgment.

These files are synthetic development fixtures. They test the v3.4 data structure and Python calculations only. They are not source-grounded benchmark evidence and must not be used for theological or model-performance claims.

The integrated prototype script is:

    scripts/ctsb_v3_4_prototype.py

Validate the fixture:

    .venv/bin/python scripts/ctsb_v3_4_prototype.py validate

Run the deterministic offline prototype:

    .venv/bin/python scripts/ctsb_v3_4_prototype.py run --backend mock

Run automated tests:

    .venv/bin/python tests/test_ctsb_v3_4_prototype.py
