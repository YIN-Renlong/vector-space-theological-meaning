# CTSB v3.5-beta Design Plan

## Status

CTSB v3.5-beta is planned but not yet implemented or frozen.

It follows the technically successful but non-evidential CTSB v3.5-alpha 100-concept experiment.

## Central beta purpose

The alpha demonstrated that the instrument and Azure pipeline work. It also showed that generated shared fields and repeated templates can build expected register separation into the benchmark.

Beta must therefore test whether CTSB can measure theological adequacy under more natural and less construction-dependent semantic competition.

## Beta research priority

The principal target is not explicit-label responsiveness.

The target is:

> Whether theological substance remains accessible under natural ambiguity and semantic competition, and whether Catholic framing corresponds to substantive Catholic representation rather than surface labelling.

## Phase B1 — Focused construction pilot

Begin with approximately 12 strategically selected audits rather than immediately rewriting all 100.

The pilot should cover:

- teleological compression;
- anthropological narrowing;
- critical-context behaviour;
- normatively conflicting registers;
- valid-but-partial registers;
- alternative lexical senses;
- generic-religious substitution;
- and framing–content divergence.

Suggested concepts:

1. freedom;
2. conscience;
3. human dignity;
4. disability;
5. death;
6. grief;
7. suicide;
8. euthanasia;
9. love;
10. grace;
11. judgment after death;
12. resurrection or Eucharist.

## Phase B2 — Separate construction streams

References, queries, and validation passages should not be generated from one shared sentence field.

Use separate processes:

- **Reference stream:** defines Catholic and comparison semantic fields.
- **Query stream:** writes natural utterances without copying anchor language.
- **Validation stream:** creates separately authored clear-register, integrative, and critical passages.
- **Review stream:** checks theological and disciplinary accuracy when time and reviewers permit.

If human review remains deferred, every beta item must remain marked non-evidential.

## Phase B3 — Reference improvements

Beta references should:

- avoid repeated stock introductions;
- avoid placing “Catholic” in every Catholic anchor body;
- carry Catholic provenance in metadata rather than relying on labels;
- vary syntax and vocabulary;
- remain conceptually balanced in length and specificity;
- distinguish Catholic-specific doctrine from generic religiosity;
- and record quotation, paraphrase, summary, generated draft, and review status accurately.

## Phase B4 — Query improvements

Primary beta queries should be:

- natural;
- plausible as user language;
- morally or pastorally meaningful;
- semantically ambiguous where appropriate;
- independent of exact reference wording;
- and varied in grammatical structure.

The explicit Catholic condition remains a diagnostic control.

The label-free theological condition should preserve equivalent content without the Catholic label.

## Phase B5 — Construction-leakage diagnostics

Before model evaluation, calculate:

- exact duplicate counts;
- token overlap;
- bigram and trigram overlap;
- longest shared phrase;
- reference-query overlap;
- reference-validation overlap;
- template-frequency concentration;
- Catholic-label frequency by register;
- text-length distributions;
- and source-field reuse.

Thresholds must be declared before viewing ambiguous-query results.

## Phase B6 — Validation and calibration

Validation should calibrate interpretation rather than merely classify obviously templated passages.

Use separate clear-register distributions to examine:

- Catholic-reference recall;
- comparison-reference recall;
- balanced accuracy;
- macro F1;
- confusion matrices;
- the distribution of $S_C$ and $S_R$ for each validated class;
- and uncertainty near the decision boundary.

Joint accessibility should be interpreted relative to validated component-score distributions, not an arbitrary universal cosine threshold.

## Phase B7 — Framing–content divergence

Predefine a concept-level flag using multiple indicators rather than one CAS value.

Candidate indicators include:

- explicit Catholic framing with weak Catholic-reference proximity relative to validated Catholic texts;
- comparison references remaining top-ranked;
- explicit-label improvement without comparable label-free content recovery;
- positive $\Delta CAS$ with non-positive $\Delta S_C$;
- generic-religious references outranking Catholic-specific references;
- instability across natural paraphrases;
- and persistence under leave-one-reference-out analysis.

The final rule must be frozen before beta Azure results are inspected.

## Phase B8 — Critical-context safeguards

Critical passages require separate attention to:

- clinical validity;
- safety relevance;
- theological and pastoral adequacy;
- non-stigmatising language;
- and the distinction between necessary clinical salience and theological exclusion.

Strong mental-health association in suicide language must not automatically be classified as attenuation.

## Phase B9 — Beta acceptance gate

Before a beta Azure run:

1. all schemas pass;
2. no accidental duplicate IDs or texts remain;
3. label-free/explicit pairs are true minimal pairs;
4. construction-overlap diagnostics meet predeclared criteria;
5. validation texts are separately authored;
6. critical passages carry ethical-review status;
7. component and sensitivity tests pass;
8. the benchmark is frozen and hashed;
9. the evidential status is explicit;
10. the working tree is clean.

## Deferred final requirements

A publication-quality benchmark still requires:

- exact source verification;
- Catholic theological review;
- relevant disciplinary review;
- independent held-out validation;
- disagreement resolution;
- statistical-plan freeze;
- and a final post-freeze model run.

## Dashboard policy

No beta dashboard should be developed until the numerical instrument and benchmark are stable.
