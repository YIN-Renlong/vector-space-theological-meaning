# Vector Space and Theological Meaning

**Measuring Secular Semantic Priors in Large Language Model Embeddings**

This repository contains a theological embedding-space audit pipeline. It measures whether general-purpose sentence embedding models associate theological concepts more closely with Catholic-magisterial descriptors or with secular/common-language contrast descriptors.

Public dashboard:

    https://yin-renlong.github.io/vector-space-theological-meaning/

## Current Method

The current pipeline uses Azure OpenAI embeddings and calculates a Catholic Alignment Score.

    Catholic Alignment Score = mean cosine(query, Catholic descriptors) - mean cosine(query, secular descriptors)

Interpretation:

- Positive CAS: closer to Catholic-magisterial descriptors.
- Negative CAS: closer to secular/common-language descriptors.
- Context Shift: theological CAS minus neutral CAS.

This is a semantic representational audit. It is not a claim that an embedding model has belief, intention, soul, or literal metaphysical ontology.

## Benchmark Files

Main draft benchmark:

    data/benchmarks/ctsb_100_v1_draft.csv

Compact descriptor source:

    data/benchmarks/ctsb_100_concepts_descriptors_v1_draft.csv

Pilot benchmark:

    data/benchmarks/ctsb_pilot.csv

The CTSB-100 draft contains:

- 100 theological concepts
- 4 theological loci
- 3 neutral query templates per concept
- 3 theological query templates per concept
- 5 Catholic-magisterial descriptors per concept
- 5 secular/common-language descriptors per concept
- 600 query rows total

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

Default full draft benchmark:

    python3 scripts/audit_azure_embeddings.py --open

Faster run without UMAP:

    python3 scripts/audit_azure_embeddings.py --skip-umap --open

Pilot benchmark:

    python3 scripts/audit_azure_embeddings.py \
      --benchmark data/benchmarks/ctsb_pilot.csv \
      --output-csv outputs/results/ctsb_pilot_results.csv \
      --output-condition-csv outputs/results/ctsb_pilot_condition_summary.csv \
      --output-concept-csv outputs/results/ctsb_pilot_concept_summary.csv \
      --output-stats-csv outputs/results/ctsb_pilot_statistical_summary.csv \
      --open

## Generated Outputs

The full audit generates:

    outputs/results/ctsb_100_results.csv
    outputs/results/ctsb_100_condition_summary.csv
    outputs/results/ctsb_100_concept_summary.csv
    outputs/results/ctsb_100_statistical_summary.csv
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

## GitHub Pages

This project is configured for GitHub Pages from:

- branch: `main`
- folder: `/`

Expected URL:

    https://yin-renlong.github.io/vector-space-theological-meaning/
