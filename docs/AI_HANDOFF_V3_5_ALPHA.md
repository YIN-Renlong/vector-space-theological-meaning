# AI Handoff: CTSB v3.5-alpha

> **Completion notice — 13 July 2026:** CTSB v3.5-alpha is complete as a generated, non-evidential 100-concept development experiment. The successful Azure run and analysis are recorded in `DEVELOPMENT_LOG.md`. The active continuation document is [AI_HANDOFF_V3_5_BETA.md](AI_HANDOFF_V3_5_BETA.md). This alpha handoff is retained as a milestone record.

## Continuation instruction

You are continuing the project **Vector Space and Theological Meaning**.

Read, in order:

1. `README.md`;
2. this handoff;
3. `docs/CTSB_V3_5_ALPHA_PROTOCOL.md`;
4. `data/benchmarks/v3_5_alpha/README.md`;
5. the CTSB v3.4 methodology sections in the root README;
6. the active v3.5-alpha generator and tests.

CTSB v3.5-alpha inherits the CTSB v3.4 mathematical instrument.

Do not:

- restore the broad v2 secular/common-language category;
- describe generated references as quotations or verified paraphrases;
- describe generated validation as independent held-out validation;
- interpret mock results as semantic evidence;
- present Azure alpha results as validated theological findings;
- begin dashboard work;
- expose or request local secrets;
- commit raw vectors, caches, outputs, backups, or `.env`.

## Current stage

The project now contains a generated exploratory 100-concept alpha benchmark.

Current generated counts:

- 100 audits;
- 600 references;
- 1,624 queries;
- 808 validation passages;
- 600 clear-register validation passages;
- eight critical-context audits;
- 25 concepts in each theological locus.

The five v3.4 audits remain integrated:

- `death_biological`;
- `grief_psychological`;
- `euthanasia_assisted_dying`;
- `grace_lexical`;
- `judgment_after_death_generic`.

## Evidential status

All alpha references and validation passages are generated and unreviewed.

The reference registry records candidate source classes, but exact source passages, exact locations, and wording fidelity have not been verified.

The alpha can support implementation and generated-benchmark-relative exploratory claims only.

Human source verification and theological or disciplinary review are formally deferred to future work and remain mandatory before evidential use.

## Mock result

The deterministic mock run passed the core data-flow checks:

- 100 audits were present;
- the five v3.4 audits were retained;
- all strict generated label pairs were valid;
- CAS reconstruction was numerically exact within floating-point precision;
- shift decomposition was numerically exact within floating-point precision;
- all query scores were finite;
- and manifest hashes verified.

The mock's perfect generated validation score is not evidential. It reflects shared generated fields and lexical templates.

## Immediate next action

After safeguards, automated tests, documentation, and Git state are confirmed:

1. run Azure/OpenAI `text-embedding-3-large`;
2. preserve all generated outputs locally;
3. inspect model metadata and dimensions;
4. verify CAS and shift identities;
5. inspect generated development-validation diagnostics;
6. inspect leave-one-reference-out stability;
7. inspect paraphrase stability;
8. analyse \(S_C\), \(S_R\), and CAS separately;
9. label every result non-evidential and generated-benchmark-relative;
10. decide whether the generated design is informative enough to justify later source review.

## Standard commands

Validate:

    .venv/bin/python scripts/ctsb_v3_5_alpha.py validate

Run tests:

    .venv/bin/python tests/test_ctsb_v3_5_alpha.py

Run mock:

    .venv/bin/python scripts/ctsb_v3_5_alpha.py run --backend mock

Future Azure run:

    .venv/bin/python scripts/ctsb_v3_5_alpha.py run --backend azure

Do not print `.env`. The Azure integration reads it locally.
