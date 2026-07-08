# Vector Space and Theological Meaning

**Measuring Secular Semantic Priors in Large Language Model Embeddings**

This repository contains a theological embedding-space audit pipeline. It measures whether general-purpose sentence embedding models associate theological concepts more closely with Catholic-magisterial descriptors or with secular/common-language contrast descriptors.

Public dashboard:

    https://yin-renlong.github.io/vector-space-theological-meaning/

## Iteration History

### CTSB-100 v1 draft

Version 1 is archived at:

    archive/ctsb_100_v1_draft/

It was the first successful 100-concept benchmark run. It used two query conditions:

1. neutral/academic wording;
2. explicit theological/Catholic wording.

It remains a valid methodological starting point because it demonstrated that the pipeline, Catholic Alignment Score, rank-order metrics, and concept-level statistical analysis work.

### CTSB-100 v2 context draft

Version 2 is now the active benchmark. It separates four query contexts:

1. bare/minimal: `love`, `freedom`, `body`;
2. ordinary lived usage: ordinary/everyday usage templates;
3. neutral academic usage: concept/meaning/discussion templates;
4. explicit Catholic/theological usage: Catholic theology/teaching/Christian doctrine templates.

This makes the analysis more precise because it distinguishes ordinary-language secular priors from academic abstraction and explicit theological code-switching.

## Current Method

The current pipeline uses Azure OpenAI embeddings and calculates a Catholic Alignment Score.

    Catholic Alignment Score = mean cosine(query, Catholic descriptors) - mean cosine(query, secular descriptors)

Interpretation:

- Positive CAS: closer to Catholic-magisterial descriptors.
- Negative CAS: closer to secular/common-language descriptors.
- Context Shift: theological CAS minus neutral CAS.

This is a semantic representational audit. It is not a claim that an embedding model has belief, intention, soul, or literal metaphysical ontology.

## Benchmark Files

Main active draft benchmark:

    data/benchmarks/ctsb_100_v2_contexts_draft.csv

Archived v1 benchmark:

    archive/ctsb_100_v1_draft/

Active compact descriptor source:

    data/benchmarks/ctsb_100_concepts_descriptors_v2_draft.csv

Archived compact descriptor source:

    data/benchmarks/ctsb_100_concepts_descriptors_v1_draft.csv

Pilot benchmark:

    data/benchmarks/ctsb_pilot.csv

The CTSB-100 v2 draft contains:

- 100 theological concepts
- 4 theological loci
- 1 bare/minimal query per concept
- 3 ordinary lived-usage query templates per concept
- 3 neutral academic query templates per concept
- 3 explicit Catholic/theological query templates per concept
- 5 Catholic-magisterial descriptors per concept
- 5 secular/common-language descriptors per concept
- 1000 query rows total

The four loci are:

1. Sin, grace, and redemption
2. Love, communion, and sacramentality
3. Human dignity and theological anthropology
4. Freedom, truth, and moral teleology

## Important Status Note

CTSB-100 v1 is a **draft** benchmark. It is suitable for exploratory analysis and pipeline testing.

Before using it for final dissertation claims, the benchmark should be:

1. theologically reviewed;
2. checked for descriptor balance;
3. frozen before final model evaluation;
4. tagged in GitHub as a stable benchmark version.

## Local Setup

Create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

Copy `.env.example` to `.env` and fill in your Azure details:

    AZURE_OPENAI_API_KEY=your_key_here
    AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large-prova1
    AZURE_OPENAI_API_VERSION=2024-02-01

Do not commit `.env`.

## Run the CTSB-100 Audit

Default full v2 draft benchmark:

    .venv/bin/python scripts/audit_azure_embeddings.py --open

Faster run without UMAP:

    .venv/bin/python scripts/audit_azure_embeddings.py --skip-umap --open

Pilot benchmark:

    python3 scripts/audit_azure_embeddings.py \
      --benchmark data/benchmarks/ctsb_pilot.csv \
      --output-csv outputs/results/ctsb_pilot_results.csv \
      --output-condition-csv outputs/results/ctsb_pilot_condition_summary.csv \
      --output-concept-csv outputs/results/ctsb_pilot_concept_summary.csv \
      --output-stats-csv outputs/results/ctsb_pilot_statistical_summary.csv \
      --open

## Generated Outputs

The active v2 audit generates:

    outputs/results/ctsb_100_v2_results.csv
    outputs/results/ctsb_100_v2_condition_summary.csv
    outputs/results/ctsb_100_v2_concept_summary.csv
    outputs/results/ctsb_100_v2_statistical_summary.csv
    index.html

The dashboard includes:

- summary metrics;
- statistical tests;
- CAS distributions;
- neutral-to-theological slope plot;
- locus-level comparison;
- concept heatmap;
- global query-only UMAP;
- per-locus UMAPs;
- concept-level table;
- raw query-level table.

UMAP is illustrative only. Substantive conclusions should rely on high-dimensional cosine, rank-order metrics, confidence intervals, and effect sizes.

## Model Metadata

The dashboard records:

- Azure deployment name
- API version
- model name: `text-embedding-3-large`
- model version: `1`
- lifecycle status: `GenerallyAvailable`
- creation/update dates
- retirement date

The displayed benchmark path is privacy-safe and does not expose the local machine path.

## Statistical Interpretation

The main statistical unit is the **concept**, not every individual query-descriptor comparison.

Main tests:

1. neutral CAS vs zero;
2. theological CAS vs zero;
3. context shift vs zero;
4. locus-level context shift;
5. concept-type context shift.

A statistically significant result should not be interpreted as proof of ontology. The appropriate conclusion is evidence of a systematic representational prior.

## Life and Death Supplement

A focused life/death benchmark has been added as a supplement because life and death are ultimate theological, existential, biological, and secular questions.

Benchmark:

    data/benchmarks/life_death_v1_draft.csv

Descriptor source:

    data/benchmarks/life_death_concepts_descriptors_v1_draft.csv

Outputs:

    outputs/results/life_death_v1_results.csv
    outputs/results/life_death_v1_condition_summary.csv
    outputs/results/life_death_v1_concept_summary.csv
    outputs/results/life_death_v1_statistical_summary.csv

Focused dashboard:

    life_death.html

Local run:

    .venv/bin/python scripts/audit_life_death_embeddings.py --open

The main dashboard also includes a hidden raw-data panel for the life/death supplement only, so that the supplemental data can be copied without copying the full CTSB-100 dataset.

## GitHub Pages

This project is configured for GitHub Pages from:

- branch: `main`
- folder: `/`

Expected URL:

    https://yin-renlong.github.io/vector-space-theological-meaning/


## Advanced Raw Data Export

The generated dashboard includes a hidden-by-default raw data section. Open the details blocks to copy or download:

- statistical summary CSV;
- concept-level summary CSV;
- condition-level summary CSV;
- raw query-level result CSV.

This is intended to make peer review and external analysis easier.
