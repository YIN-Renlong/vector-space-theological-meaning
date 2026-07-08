# Statistical Analysis Plan

## Unit of Analysis

The main statistical unit is the concept.

The CTSB-100 draft has 100 concepts. Each concept has multiple query templates and descriptor comparisons, but those comparisons are nested under the concept. They improve measurement reliability but should not be treated as fully independent observations.

## Primary Metrics

For a query:

    CatholicScore = mean cosine(query, Catholic descriptors)

    SecularScore = mean cosine(query, secular descriptors)

    Catholic Alignment Score = CatholicScore - SecularScore

For each concept:

    Neutral CAS = mean CAS across neutral templates

    Theological CAS = mean CAS across theological templates

    Context Shift = Theological CAS - Neutral CAS

## Main Tests

1. Neutral CAS vs zero

   Tests whether neutral queries are closer to Catholic or secular descriptors.

2. Theological CAS vs zero

   Tests whether explicitly theological queries are closer to Catholic or secular descriptors.

3. Context Shift vs zero

   Tests whether explicit theological framing moves embeddings toward Catholic-magisterial descriptors.

4. Locus-level tests

   Tests whether the four theological loci behave differently.

5. Concept-type tests

   Tests whether doctrinal, anthropological, sacramental, social-ethical, and juridical concepts behave differently.

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
