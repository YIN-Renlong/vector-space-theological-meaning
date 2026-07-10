# CTSB-100 v2 Context Draft Archive

This folder is the frozen project snapshot immediately before the CTSB v3.4 methodology redesign.

## Status

- Archive version: CTSB-100 v2 context draft
- Archived: 10 July 2026
- Audited model: Azure/OpenAI `text-embedding-3-large`
- Benchmark status: exploratory draft requiring theological and construct validation
- Git tag: `ctsb-v2-context-draft-2026-07-10`

This archive is retained for transparency, reproducibility, and comparison with the redesigned v3.4 methodology. It must not be confused with the active v3.4 protocol.

## Archived documentation

- [Project README at v2](README_project_at_v2.md)
- [v2 statistical analysis plan](docs/statistical_analysis_plan.md)
- [Main v2 dashboard](index_v2_dashboard.html)
- [Life and Death v1 supplement dashboard](life_death_v1_dashboard.html)

## Archived materials

- `data/`: v2 benchmark inputs and the Life and Death supplement
- `scripts/`: v2 Azure embedding-audit scripts
- `outputs/results/`: query-, condition-, concept-, and statistical-level CSV outputs
- `outputs/img/`: exported v2 figures
- `requirements_v2.txt`: v2 Python dependencies

The archive includes some earlier files that were still present in the v2 working tree. The separately curated v1 archive remains at:

- [CTSB-100 v1 draft archive](../ctsb_100_v1_draft/README.md)

## Embedding cache

The local Azure embedding cache is moved into this archive when available, but it is excluded from Git by `.gitignore`. It may therefore be present locally but absent from a GitHub clone.

The numerical result tables remain publicly archived and do not require the cache for inspection.

## Public archival dashboards

- Main v2 dashboard:
  https://yin-renlong.github.io/vector-space-theological-meaning/archive/ctsb_100_v2_context_draft/index_v2_dashboard.html

- Life and Death v1 dashboard:
  https://yin-renlong.github.io/vector-space-theological-meaning/archive/ctsb_100_v2_context_draft/life_death_v1_dashboard.html

## Interpretation warning

The v2 descriptor sets combined ordinary, psychological, biological, clinical, legal, economic, social, and generic religious meanings under an overly broad comparison category. A negative v2 CAS should therefore be interpreted only as greater mean cosine similarity to the selected v2 comparison descriptors.

The v3.4 redesign addresses this limitation by:

1. defining comparison registers explicitly;
2. distinguishing complementary, partial, conflicting, lexical, and generic-religious relations;
3. grounding Catholic references in identifiable sources;
4. validating the metric on held-out texts;
5. decomposing contrast shifts into their Catholic and comparison components;
6. adding natural ambiguity and critical-context tests.
