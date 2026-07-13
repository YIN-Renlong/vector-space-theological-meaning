# CTSB v3.5-alpha generated exploratory run

## Evidential status

**NON-EVIDENTIAL GENERATED DEVELOPMENT ANALYSIS.**

The references and validation passages were generated for instrument development. They have not received exact-source, theological, disciplinary, ethical, or linguistic review.

All results are relative to this generated benchmark and must not be presented as validated findings about Catholic theology, pastoral adequacy, model bias, or embedding models in general.

## Input counts

- audits: 100
- references: 600
- queries: 1624
- validation_texts: 808
- clear_validation_texts: 600
- expected_alpha_audits: 100
- generated_references: 600
- generated_queries: 1624
- generated_validation_texts: 808
- critical_audits: 8

## Generated development-validation diagnostic

- balanced accuracy: 1.0000
- Catholic recall: 1.0000
- comparison recall: 1.0000
- macro F1: 1.0000

These values are pipeline diagnostics, not independent held-out validation.

## Condition-level generated benchmark summary

| Condition | Concepts | Mean S_C | Mean S_R | Mean CAS | Median CAS |
|---|---:|---:|---:|---:|---:|
| bare | 100 | 0.4679 | 0.5021 | -0.0342 | -0.0372 |
| natural_general | 100 | 0.5166 | 0.7600 | -0.2434 | -0.2474 |
| natural_ambiguous | 100 | 0.4900 | 0.4963 | -0.0063 | -0.0086 |
| label_free_theological | 100 | 0.8067 | 0.5224 | 0.2843 | 0.2774 |
| explicit_catholic | 100 | 0.8919 | 0.4694 | 0.4226 | 0.4220 |
| integrative | 100 | 0.7094 | 0.6757 | 0.0338 | 0.0322 |
| critical | 8 | 0.3966 | 0.4198 | -0.0232 | -0.0305 |

## Matched-shift generated benchmark summary

| Contrast | Concepts | Mean Delta S_C | Mean Delta S_R | Mean Delta CAS | Positive Delta CAS |
|---|---:|---:|---:|---:|---:|
| bare_to_general | 100 | 0.0487 | 0.2579 | -0.2092 | 0.0000 |
| general_to_ambiguous | 100 | -0.0267 | -0.2637 | 0.2370 | 1.0000 |
| general_to_label_free_theological | 100 | 0.2901 | -0.2376 | 0.5277 | 1.0000 |
| label_free_to_explicit_catholic | 100 | 0.0852 | -0.0531 | 0.1383 | 1.0000 |
| general_to_integrative | 100 | 0.1928 | -0.0844 | 0.2772 | 1.0000 |
| general_to_critical | 8 | -0.0752 | -0.3302 | 0.2550 | 1.0000 |

## Required future review before evidential use

1. Verify every proposed source and exact source location.
2. Replace generated references with reviewed quotations, close paraphrases, or clearly identified summaries.
3. Obtain Catholic theological review.
4. Obtain relevant medical, psychological, legal, lexical, bioethical, and religious-studies review.
5. Create genuinely independent held-out validation passages.
6. Complete ethical review of critical and crisis-language texts.
7. Freeze and hash the reviewed benchmark before any final Azure run.

No dashboard should be built from this alpha run.
