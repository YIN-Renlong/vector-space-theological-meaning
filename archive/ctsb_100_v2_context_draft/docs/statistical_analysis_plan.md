# Statistical Analysis Plan

## Version

Active benchmark:

    CTSB-100 v2 context draft

Archived benchmark:

    archive/ctsb_100_v1_draft/

## Unit of Analysis

The main statistical unit is the concept.

The CTSB-100 v2 draft has 100 concepts. Each concept has multiple query templates and descriptor comparisons, but those comparisons are nested under the concept. They improve measurement reliability but should not be treated as fully independent observations.

## Query Conditions

Version 2 separates four query contexts:

1. bare/minimal;
2. ordinary lived usage;
3. neutral academic usage;
4. explicit Catholic/theological usage.

This distinction is important because an embedding model may behave differently when queried by a bare term, ordinary-language phrase, academic abstraction, or explicit theological framing.

## Primary Metrics

For a query:

    CatholicScore = mean cosine(query, Catholic descriptors)

    SecularScore = mean cosine(query, secular descriptors)

    Catholic Alignment Score = CatholicScore - SecularScore

For each concept:

    Bare CAS = mean CAS for bare/minimal query

    Ordinary CAS = mean CAS across ordinary lived-usage templates

    Academic CAS = mean CAS across neutral academic templates

    Catholic CAS = mean CAS across explicit Catholic/theological templates

Primary shift metric:

    Ordinary to Catholic Shift = Catholic CAS - Ordinary CAS

Secondary shift metrics:

    Bare to Catholic Shift = Catholic CAS - Bare CAS

    Academic to Catholic Shift = Catholic CAS - Academic CAS

## Main Tests

1. Bare CAS vs zero.

2. Ordinary CAS vs zero.

3. Academic CAS vs zero.

4. Catholic CAS vs zero.

5. Ordinary to Catholic Shift vs zero.

6. Academic to Catholic Shift vs zero.

7. Locus-level tests for the four theological loci.

8. Concept-type exploratory tests.

## Interpretation Rules

A result is more persuasive when it has:

- confidence interval excluding zero;
- non-trivial effect size;
- directional consistency across many concepts;
- theological interpretability;
- robustness across loci and query templates.

A p-value alone is not enough.

## Practical Effect Heuristic

Approximate CAS interpretation:

- below 0.02: negligible
- 0.02 to 0.05: small
- 0.05 to 0.10: meaningful
- above 0.10: strong

These are heuristic thresholds, not universal laws.

## No-Difference Claims

A non-significant result does not prove no difference. It means the test did not find enough evidence for a difference.

A stronger no-difference claim requires an equivalence design. This project uses a provisional negligible band of ±0.02 for interpretive caution.

## Visualization Rules

UMAP is exploratory. UMAP coordinates should not be treated as absolute theological or semantic distances.

Primary evidence remains:

- high-dimensional cosine;
- rank-order metrics;
- concept-level CAS;
- confidence intervals;
- effect sizes.

## Benchmark Status

CTSB-100 v2 is still a draft benchmark. Before final dissertation claims, the descriptor sets should be reviewed, frozen, and tagged.
