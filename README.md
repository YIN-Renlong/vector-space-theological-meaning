# Vector Space and Theological Meaning

**Measuring Secular Semantic Priors in Large Language Model Embeddings**

This repository contains the computational materials for a theological embedding-space audit. The project investigates whether general-purpose sentence embedding models encode semantic associations that diverge from Catholic magisterial usage, especially in concepts related to sin, love, human dignity, and freedom.

The current repository begins with a small Azure OpenAI pilot benchmark and is structured so that it can later scale to a 100-concept Catholic Theological Semantic Benchmark.

## Research Summary

This project asks whether general-purpose AI embedding models associate theological concepts more closely with secular/common-language descriptors than with Catholic-magisterial descriptors.

The project does not claim that embedding models possess beliefs, souls, intentions, or a literal metaphysical ontology. Instead, it treats embedding spaces as measurable representational systems whose semantic neighborhoods can reveal statistically testable priors.

A concise version of the research claim:

> This dissertation investigates whether general-purpose sentence embedding models encode secular semantic priors that diverge from Catholic magisterial usage. It constructs a Catholic theological benchmark across four loci: sin/grace, love/communion, human dignity/anthropology, and freedom/truth. Using cosine-similarity deltas, rank-order metrics, and concept-level statistical tests, it compares commercial and open-source baseline embeddings with a Catholic-domain adapted reference model trained on a curated magisterial corpus. The results are interpreted not as proof of machine belief or ontology, but as evidence of representational tendencies with implications for theological HCI and pastoral AI design.

## Research Questions

1. Do general-purpose embedding models associate selected theological concepts more closely with secular/common-language descriptors than with Catholic-magisterial descriptors?

2. Does explicit theological context alter those associations?

3. Does domain adaptation on a Catholic magisterial corpus shift an open-source embedding model toward Catholic-magisterial semantic associations?

4. What are the implications of these representational priors for theological HCI, pastoral AI, and domain-sensitive AI design?

## Repository Structure

    vector-space-theological-meaning/
    ├── README.md
    ├── LICENSE
    ├── .gitignore
    ├── .env.example
    ├── .nojekyll
    ├── requirements.txt
    ├── index.html
    ├── data/
    │   └── benchmarks/
    │       ├── ctsb_pilot.csv
    │       └── ctsb_100_seed_concepts.csv
    ├── outputs/
    │   └── results/
    │       └── .gitkeep
    └── scripts/
        └── audit_azure_embeddings.py

## Current Status

This repository currently supports:

- Azure OpenAI embedding audit using `text-embedding-3-large` or another Azure embedding deployment.
- Pilot benchmark across four theological loci.
- Neutral versus explicitly Catholic query conditions.
- Catholic-magisterial descriptor comparison.
- Secular/common-language descriptor comparison.
- Cosine similarity calculation.
- Catholic Alignment Score calculation.
- Rank-order summary.
- CSV result export.
- Static Plotly dashboard generation as `index.html`.
- GitHub Pages hosting from the repository root.

The current pilot is not intended to be the final statistical study. It is a reproducible proof of method. The intended dissertation-scale version should use approximately 100 concepts.

## Important Methodological Discipline

This project uses careful language.

It does not say:

- The model is literally Catholic, secular, Pelagian, materialist, or libertarian.
- Cosine similarity proves metaphysical truth.
- OpenAI embeddings are the internal source code of ChatGPT.
- A Catholic-domain model becomes the Magisterium.

It says:

- Embedding models can be audited as representational systems.
- Their semantic neighborhoods can encode measurable priors.
- These priors may be theologically significant for pastoral AI and theological HCI.

## Quick Start

### 1. Create a local environment

Recommended:

    cd /Users/Renlong/Projects/GitHub/YIN-Renlong/vector-space-theological-meaning
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

### 2. Configure Azure credentials

Copy `.env.example` to `.env`, then fill in your real Azure values.

Required variables:

    AZURE_OPENAI_API_KEY=your_key_here
    AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large-prova1
    AZURE_OPENAI_API_VERSION=2024-02-01

Do not commit `.env`. It is ignored by Git.

### 3. Run the pilot audit

    python3 scripts/audit_azure_embeddings.py

This will generate:

    outputs/results/ctsb_pilot_results.csv
    index.html

### 4. Preview locally

    python3 -m http.server 8000

Then open:

    http://localhost:8000

Hard refresh if needed:

    Command + Shift + R

## Azure Model

The default deployment name in the script is read from:

    AZURE_OPENAI_EMBEDDING_DEPLOYMENT

For the current pilot, this can be:

    text-embedding-3-large-prova1

The script does not hard-code your API key or endpoint. It reads them from `.env`.

## Benchmark Format

The pilot benchmark is stored here:

    data/benchmarks/ctsb_pilot.csv

Each row contains:

- `locus`
- `concept`
- `query_condition`
- `query`
- `catholic_descriptors`
- `secular_descriptors`

Descriptor fields use `||` as a separator.

Example structure:

    locus,concept,query_condition,query,catholic_descriptors,secular_descriptors
    Sin Grace and Redemption,sin,neutral,The concept of sin.,rupture of communion with God||offense against divine love,legal crime||social rule-breaking

## Current Pilot Loci

The pilot benchmark uses four theological loci:

1. Sin, grace, and redemption
2. Love, communion, and sacramentality
3. Human dignity and theological anthropology
4. Freedom, truth, and moral teleology

The pilot tests four central concepts:

- sin
- love
- human person
- freedom

Each concept has:

- one neutral query
- one explicitly Catholic/theological query
- five Catholic-magisterial descriptors
- five secular/common-language contrast descriptors

## Scaling to CTSB-100

The dissertation-scale benchmark should use approximately 100 concepts, distributed across four loci:

| Locus | Approximate Concepts |
|---|---:|
| Sin, grace, and redemption | 25 |
| Love, communion, and sacramentality | 25 |
| Human dignity and theological anthropology | 25 |
| Freedom, truth, and moral teleology | 25 |

The file below contains a provisional 100-concept seed list:

    data/benchmarks/ctsb_100_seed_concepts.csv

This seed file is not yet a complete benchmark because it does not include descriptor sets. Before final statistical testing, each concept should receive carefully validated Catholic and secular descriptor sets.

## Catholic Alignment Score

For a query phrase `q`, a Catholic descriptor set `C`, and a secular descriptor set `S`, the script calculates:

    CatholicScore(q) = mean cosine(q, c) for c in C

    SecularScore(q) = mean cosine(q, s) for s in S

    CatholicAlignmentScore(q) = CatholicScore(q) - SecularScore(q)

Interpretation:

- Positive CAS: the query is closer to Catholic-magisterial descriptors.
- Negative CAS: the query is closer to secular/common-language descriptors.
- Near-zero CAS: no clear directional preference.

This is an operational metric, not metaphysical proof.

## Rank-Order Metrics

The script also records:

- nearest Catholic descriptor
- nearest secular descriptor
- top descriptor overall
- whether the top descriptor is Catholic or secular
- rank of the nearest Catholic descriptor
- rank of the nearest secular descriptor

Rank-order metrics are useful because small cosine differences may be statistically measurable but hard to interpret theologically.

## Dashboard

Running the script produces a static dashboard:

    index.html

The dashboard contains:

- summary methodology note
- Catholic Alignment Score bar chart
- 3D UMAP visualization
- result table with raw scores

The UMAP plot is illustrative only. The primary evidence remains the high-dimensional cosine and rank-order metrics.

## GitHub Pages

The repository is configured for GitHub Pages from:

- Branch: `main`
- Folder: `/`

Expected public URL:

    https://yin-renlong.github.io/vector-space-theological-meaning/

After pushing new generated results, GitHub Pages may take a few minutes to refresh.

## Reproducibility Notes

The script records:

- benchmark file
- Azure deployment name
- API version
- generated timestamp
- number of benchmark rows
- number of unique embedded strings

Embeddings are cached locally in:

    outputs/cache/

The cache is ignored by Git to avoid committing large vector files. The generated dashboard and CSV results can be committed.

## Statistical Design for the Final Dissertation

The pilot is small and should not be used for broad statistical claims.

For the full dissertation:

- use approximately 100 concepts;
- treat the concept as the main statistical unit;
- use multiple query templates per concept;
- use multiple Catholic descriptors and secular descriptors;
- validate descriptor sets theologically;
- compare neutral and theological query conditions;
- compare commercial baseline models with open-source baseline models;
- compare an open-source base model with a Catholic-domain adapted version of the same model.

Recommended statistical methods:

- concept-level Catholic Alignment Score;
- paired tests for neutral versus theological context;
- paired tests for base versus adapted model;
- bootstrapped confidence intervals;
- Wilcoxon signed-rank tests if distributions are non-normal;
- mixed-effects model if the dataset becomes large enough;
- multiple-comparison correction for per-concept tests.

## Theological Interpretation

The four main theological loci should be interpreted carefully.

### Sin, Grace, and Redemption

The project should ask whether sin is represented primarily as:

- legal wrongdoing;
- social deviance;
- psychological guilt;

or as:

- rupture of communion with God;
- loss of charity;
- need for grace;
- repentance and reconciliation.

Avoid immediately claiming that a model is “Pelagian.” A more precise claim is that the model may privilege juridical, sociological, or moralistic associations over grace-centered ones.

### Love, Communion, and Sacramentality

The project should ask whether love is represented primarily as:

- romance;
- attraction;
- affective attachment;

or as:

- caritas;
- self-gift;
- love of God and neighbor;
- sacrificial communion.

Catholic theology does not simply reject eros, so the analysis should avoid a simplistic eros-versus-agape opposition.

### Human Dignity and Theological Anthropology

The project should ask whether the human person is represented primarily as:

- biological organism;
- autonomous individual;
- consumer;
- data-producing user;

or as:

- imago Dei;
- unity of body and soul;
- bearer of intrinsic dignity;
- moral and spiritual subject.

Catholic theology does not deny embodiment or biological life. The concern is reductionism.

### Freedom, Truth, and Moral Teleology

The project should ask whether freedom is represented primarily as:

- autonomy;
- absence of constraint;
- maximization of choice;

or as:

- capacity to choose the good;
- truth-directed moral agency;
- responsible freedom;
- liberation from sin.

This locus is especially relevant for theological HCI because many systems are optimized around user preference and convenience.

## Limitations

1. Public embedding APIs are not the same as the internal representations of generative LLMs.
2. Cosine similarity is a semantic measurement, not ontology.
3. A Catholic-domain adapted model is not the Magisterium.
4. Corpus selection affects results.
5. English-language analysis limits generalization.
6. API models can change over time.
7. Descriptor sets require theological validation.
8. Statistical significance is not identical to theological significance.

## Roadmap

Near-term:

- Expand the pilot benchmark.
- Add 100-concept descriptor sets.
- Add validation notes for Catholic and secular descriptors.
- Add open-source baseline model evaluation.
- Add Catholic-domain adaptation pipeline.
- Add base-versus-adapted comparison.

Future work:

- Theological reward models.
- RLHF and theological value-sensitive design.
- Retrieval-augmented Catholic AI systems.
- User studies for pastoral AI.
- Multilingual theological embedding spaces.
