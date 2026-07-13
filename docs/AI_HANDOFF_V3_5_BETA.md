# AI Handoff: CTSB v3.5-beta

## Continuation instruction

You are continuing **Vector Space and Theological Meaning**.

Read, in order:

1. `README.md`;
2. this handoff;
3. `docs/CTSB_V3_5_BETA_PLAN.md`;
4. `docs/CTSB_V3_5_ALPHA_PROTOCOL.md`;
5. `data/benchmarks/v3_5_alpha/README.md`;
6. `DEVELOPMENT_LOG.md` when detailed chronology is needed;
7. the active v3.5-alpha generator, v3.4 scoring engine, and tests.

CTSB v3.5-alpha is complete as a generated, non-evidential development experiment. CTSB v3.5-beta is the next planned benchmark-development phase.

## 1. Project identity

- **Project:** Vector Space and Theological Meaning
- **Direct object:** Azure/OpenAI `text-embedding-3-large`
- **Confirmed dimensions:** 3,072
- **Current completed milestone:** CTSB v3.5-alpha
- **Next phase:** CTSB v3.5-beta
- **Alpha Git commit:** `3d8c92dfe0807363d8e424202ece7a42bc60b28c`
- **Alpha Azure run ID:** `v3_5_alpha_azure_20260713-010232`
- **Alpha evidential status:** generated, unreviewed, non-evidential
- **Current version marker:** `3.5-alpha-complete-beta-planned`

The project audits semantic representation. It does not determine theological truth, machine belief, intentional deception, or the correctness of an actual chatbot response.

## 2. Central research purpose

The project is not principally testing the predictable fact that explicit theological vocabulary moves text toward theological references.

It asks whether theological meaning remains substantively accessible when language is:

- natural rather than benchmark-like;
- ambiguous;
- morally contested;
- pastorally vulnerable;
- clinically urgent;
- or explicitly Catholic but semantically pulled toward another register.

The central concern is **theological framing–content divergence**: Catholic surface framing may coexist with a semantic representation that remains generic, reduced, displaced, or comparison-register dominant.

Use terms such as:

- default semantic tendency;
- latent representational prior;
- context-resistant register pull;
- residual comparison-register dominance;
- surface contextualisation without substantive recovery;
- and theological framing–content divergence.

Do not attribute consciousness, a subconscious, belief, hostility, or deceptive intention to the embedding model.

## 3. Controlling research questions

The complete research questions are maintained in section 4 of `README.md`.

The principal empirical questions concern:

1. default semantic foregrounding;
2. joint accessibility versus theological reduction;
3. theological legibility without an overt label;
4. context-resistant register pull under Catholic framing;
5. theological framing–content divergence;
6. genuine recovery versus apparent recovery;
7. critical and crisis-context behaviour;
8. persistent theological attenuation;
9. recurring theological patterns across loci and relationship types;
10. robustness, validation, and theological calibration.

The explicit Catholic condition is a control and secondary label-dependence test. It must not dominate the project’s conclusions.

## 4. Inherited mathematical instrument

For query $q$, Catholic reference set $C$, and specifically named comparison set $R$:

$$
S_C(q)=\frac{1}{|C|}\sum_{c\in C}\cos(e(q),e(c))
$$

$$
S_R(q)=\frac{1}{|R|}\sum_{r\in R}\cos(e(q),e(r))
$$

$$
CAS(q;C,R)=S_C(q)-S_R(q)
$$

For matched contexts:

$$
\Delta CAS=\Delta S_C-\Delta S_R
$$

Positive $\Delta CAS$ does not prove theological association gain. Positive $\Delta S_C$ must be inspected separately.

## 5. Alpha benchmark and implementation

The alpha contains:

- 100 audits;
- 25 concepts in each of four theological loci;
- 600 generated references;
- 1,624 queries;
- 808 generated validation passages;
- 600 clear-register validation passages;
- eight critical-context audits;
- three references per register per audit;
- three paraphrases for major conditions;
- strict label-free/explicit-Catholic pairs;
- leave-one-reference-out analysis;
- paraphrase sensitivity;
- bootstrap summaries;
- and paired sign-flip diagnostics.

The five v3.4 audits were retained:

- death versus biological description;
- grief versus psychological bereavement;
- euthanasia versus permissive assisted dying;
- grace versus elegance and social charm;
- judgment after death versus generic religious judgment.

The active alpha script imports the v3.4 engine rather than duplicating its mathematical implementation.

## 6. Completed testing

Five v3.4 regression tests passed.

Five v3.5-alpha tests passed:

1. 100-audit and four-locus registry balance;
2. generated table counts and schema validation;
3. preservation of source and review warnings;
4. exact label-free/explicit-Catholic pairs;
5. complete mock pipeline, manifest, CAS, decomposition, similarities, and sensitivity exports.

The deterministic mock run passed all core implementation checks.

## 7. Alpha Azure run

The successful Azure run used:

- provider: Azure OpenAI;
- deployment: `text-embedding-3-large-prova1`;
- Azure-reported model: `text-embedding-3-large`;
- dimensions: 3,072;
- unique texts: 3,032;
- new embeddings: 3,032;
- cached embeddings: 0;
- API batches: 48;
- query scores: 1,624;
- matched shifts: 1,524;
- validation scores: 808;
- reference-level similarities: 14,592.

Maximum CAS reconstruction error was approximately:

$$
2.22\times10^{-16}
$$

Maximum decomposition error was approximately:

$$
5.55\times10^{-17}
$$

All scores were finite, hashes verified, outputs were ignored by Git, and no secrets were printed or committed.

## 8. Alpha aggregate results

| Condition | Mean $S_C$ | Mean $S_R$ | Mean CAS | Positive CAS |
|---|---:|---:|---:|---:|
| Bare | 0.4679 | 0.5021 | -0.0342 | 25% |
| Natural general | 0.5166 | 0.7600 | -0.2434 | 0% |
| Natural ambiguous | 0.4900 | 0.4963 | -0.0063 | 42% |
| Label-free theological | 0.8067 | 0.5224 | +0.2843 | 100% |
| Explicit Catholic | 0.8919 | 0.4694 | +0.4226 | 100% |
| Integrative | 0.7094 | 0.6757 | +0.0338 | 70% |
| Critical | 0.3966 | 0.4198 | -0.0232 | 37.5% |

Selected mean shifts:

| Contrast | $\Delta S_C$ | $\Delta S_R$ | $\Delta CAS$ |
|---|---:|---:|---:|
| Bare to general | +0.0487 | +0.2579 | -0.2092 |
| General to ambiguous | -0.0267 | -0.2637 | +0.2370 |
| General to label-free theological | +0.2901 | -0.2376 | +0.5277 |
| Label-free to explicit Catholic | +0.0852 | -0.0531 | +0.1383 |
| General to integrative | +0.1928 | -0.0844 | +0.2772 |
| General to critical | -0.0752 | -0.3302 | +0.2550 |

The general-to-ambiguous and general-to-critical contrasts demonstrate apparent positive recovery without Catholic-reference gain.

## 9. Critical-context alpha results

Mean critical CAS:

- euthanasia: -0.1051;
- suicide: -0.0658;
- death: -0.0397;
- suffering: -0.0357;
- grief: -0.0253;
- palliative care: +0.0040;
- illness: +0.0306;
- dying: +0.0513.

These are generated cases, not pastoral findings. Strong clinical or psychological salience may be appropriate and safety-relevant.

## 10. Robustness results

- 1,461 of 1,624 queries retained the same CAS sign under every leave-one-reference-out case.
- Mean leave-one-reference-out sign stability was 0.9710.
- The largest absolute leave-one-reference-out CAS change was 0.0936.
- 137 of 508 audit-condition groups had mixed CAS signs across paraphrases.
- No audit-contrast group had mixed $\Delta CAS$ direction across paraphrases.
- Median condition CAS standard deviation was 0.0324.
- Maximum condition CAS standard deviation was 0.1339.

Absolute near-zero classifications were more fragile than the deliberately constructed shift directions.

## 11. What alpha established

Alpha established that:

- the instrument scales to 100 audits;
- Azure integration works at expanded scale;
- full reference-level scoring works;
- component decomposition prevents misleading recovery claims;
- paraphrase and reference sensitivity can be measured;
- integrative and critical contexts can be inspected separately;
- and generated-benchmark-relative label effects can be detected.

## 12. What alpha did not establish

Alpha did not establish:

- source-grounded Catholic theological performance;
- independent held-out validation;
- persistent theological attenuation;
- latent anti-theological bias;
- Catholic pastoral adequacy;
- theological framing–content divergence in natural language;
- doctrinal error in a generated response;
- or actual user deception.

The generated reference, query, and validation texts share construction fields and templates.

The perfect development-validation score of 1.0 is therefore a pipeline diagnostic, not scientific validation.

## 13. Beta objective

CTSB v3.5-beta should determine whether the instrument can begin addressing the substantive research questions rather than primarily detecting its own templates.

Beta should:

1. reduce direct phrase reuse between references and queries;
2. reduce repeated Catholic labels in Catholic reference bodies;
3. separate provenance metadata from semantic anchor wording;
4. improve natural general, ambiguous, integrative, and critical queries;
5. create separately authored development validation;
6. quantify lexical and n-gram overlap;
7. calibrate joint accessibility using validation distributions;
8. predefine framing–content divergence indicators;
9. retain component decomposition and sensitivity analysis;
10. remain non-evidential if exact source verification and human review are still deferred.

Do not run another Azure benchmark merely because beta files exist. First validate beta construction quality and freeze the beta development set.

## 14. Immediate next action

The immediate task is:

> Design a small CTSB v3.5-beta construction pilot that reduces template and label leakage, introduces separate authoring streams for references, queries, and validation, and operationalises the central research questions before regenerating all 100 audits.

A practical first beta pilot should use a strategically selected subset, including:

- freedom;
- conscience;
- human dignity;
- disability;
- death;
- grief;
- suicide;
- euthanasia;
- love;
- grace;
- judgment after death;
- and one additional generic-religious/Catholic-specific case.

Do not immediately rerun all 100 concepts.

## 15. Restrictions

- Do not restore the broad v2 secular/common-language category.
- Do not treat generated references as verified source paraphrases.
- Do not describe development validation as independently held out.
- Do not use positive CAS alone as evidence of theological recovery.
- Do not infer intention, belief, subconscious bias, or deception.
- Do not commit `.env`, caches, vectors, outputs, backups, or context bundles.
- Do not begin dashboard work.
- Do not request or expose local secrets.
- Do not compare raw CAS across embedding providers as a common calibrated scale.

## 16. Output policy

Numerical high-dimensional analysis remains primary.

Required future outputs include:

- complete query-to-reference similarities;
- $S_C$, $S_R$, and CAS;
- nearest references and ranks;
- matched component shifts;
- validation distributions;
- leave-one-reference-out sensitivity;
- paraphrase sensitivity;
- construction-overlap diagnostics;
- concept-level summaries;
- and frozen benchmark hashes.

Visualisation remains secondary.

## 17. User workflow

The user works through macOS Terminal and prefers:

- one complete Bash block per runnable step;
- `bash <<'BASH'` with `set -euo pipefail`;
- timestamped backups;
- Python `pathlib`, regex, and replacement scripts;
- no manual editor instructions unless unavoidable;
- HTTPS GitHub remotes;
- `gh` CLI;
- validation before commit;
- useful final status output;
- and lean implementation without unnecessary modules.
