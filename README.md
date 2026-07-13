# Vector Space and Theological Meaning

<!-- BEGIN V3_5_ALPHA_STATUS -->
## Active development status — 13 July 2026

**CTSB v3.5-alpha is technically complete as a generated, non-evidential 100-concept development experiment. CTSB v3.5-beta is the next planned phase.**

The alpha milestone contains:

- 100 concept-to-register audits;
- 25 concepts in each of four theological loci;
- 600 generated and unreviewed references;
- 1,624 controlled queries;
- 808 generated development-validation passages;
- eight critical-context audits;
- three natural paraphrases for major conditions;
- leave-one-reference-out analysis;
- paraphrase-sensitivity analysis;
- and the five original v3.4 audits covering death, grief, euthanasia, grace, and judgment after death.

Five v3.4 regression tests and five v3.5-alpha tests passed.

A successful Azure run on 13 July 2026 embedded 3,032 unique texts in 48 batches. Azure reported `text-embedding-3-large` with 3,072 dimensions. CAS reconstruction, shift decomposition, finite-value checks, file hashes, and expanded output generation all passed.

The principal alpha aggregate results were:

| Condition | Mean $S_C$ | Mean $S_R$ | Mean CAS |
|---|---:|---:|---:|
| Bare | 0.4679 | 0.5021 | -0.0342 |
| Natural general | 0.5166 | 0.7600 | -0.2434 |
| Natural ambiguous | 0.4900 | 0.4963 | -0.0063 |
| Label-free theological | 0.8067 | 0.5224 | +0.2843 |
| Explicit Catholic | 0.8919 | 0.4694 | +0.4226 |
| Integrative | 0.7094 | 0.6757 | +0.0338 |
| Critical | 0.3966 | 0.4198 | -0.0232 |

These results remain **generated-benchmark-relative and non-evidential**. The alpha deliberately reused generated concept fields across references, queries, and validation passages. Its perfect development-validation score therefore does not constitute independent validation. General, theological, integrative, and explicit-Catholic conditions also contain construction effects and lexical overlap.

The strongest alpha finding is methodological: CTSB can distinguish genuine Catholic-reference gain from an apparently positive relative shift caused only by a larger decline in comparison-register similarity.

The next phase, CTSB v3.5-beta, will focus on natural-language quality, construction-leakage reduction, reference-label balance, genuinely separate validation design, calibration criteria, and operational tests of theological framing–content divergence.

Read:

- [Current CTSB v3.5-beta handoff](docs/AI_HANDOFF_V3_5_BETA.md)
- [CTSB v3.5-beta design plan](docs/CTSB_V3_5_BETA_PLAN.md)
- [CTSB v3.5-alpha protocol](docs/CTSB_V3_5_ALPHA_PROTOCOL.md)
- [CTSB v3.5-alpha benchmark status](data/benchmarks/v3_5_alpha/README.md)
- [Full development log](DEVELOPMENT_LOG.md)

Dashboard work remains deferred.
<!-- END V3_5_ALPHA_STATUS -->

## CTSB v3.4 Methodology Design

**From doctrinal legibility to theological behaviour under ambiguity and critical contexts**

CTSB v3.4 redesigns the project as a source-grounded and validated theological audit of Azure/OpenAI `text-embedding-3-large`.

The active repository contains the **v3.4 methodology protocol, benchmark-construction plan, and a non-evidential synthetic development prototype**. The prototype tests data validation, differential cosine scoring, matched contextual contrasts, shift decomposition, and output generation. It is not the final v3.4 benchmark and does not provide empirical theological findings.

The previous v2 implementation has been frozen in the repository archive:

- [CTSB-100 v2 context-draft archive](archive/ctsb_100_v2_context_draft/README.md)
- [CTSB-100 v1 draft archive](archive/ctsb_100_v1_draft/README.md)

Public archival dashboards:

- [CTSB-100 v2 dashboard](https://yin-renlong.github.io/vector-space-theological-meaning/archive/ctsb_100_v2_context_draft/index_v2_dashboard.html)
- [Life and Death v1 dashboard](https://yin-renlong.github.io/vector-space-theological-meaning/archive/ctsb_100_v2_context_draft/life_death_v1_dashboard.html)

The root `index.html` and `life_death.html` remain temporarily as compatibility copies of the v2 dashboards. They are not v3.4 results.

<!-- BEGIN V3_4_CURRENT_STATUS -->
## Current status — 12 July 2026

**CTSB v3.4 Step 1 is complete.**

The project has moved from methodology design to a working, lean development prototype. The completed Step 1 includes:

- five illustrative audit units covering all five theological relationship types;
- four linked synthetic fixture tables for comparisons, references, queries, and validation passages;
- one integrated Python analysis script;
- deterministic local mock embeddings for offline testing;
- five passing automated tests;
- successful Azure embedding integration;
- confirmation that Azure returned `text-embedding-3-large` vectors with 3,072 dimensions;
- complete query-to-reference cosine exports;
- separate Catholic and comparison similarities, `S_C` and `S_R`;
- Catholic Association Contrast, `CAS = S_C - S_R`;
- nearest-reference rankings;
- matched contextual contrasts;
- and numerical verification of `Delta CAS = Delta S_C - Delta S_R`.

The Azure integration run embedded 90 synthetic fixture texts and successfully generated query scores, validation scores, reference-level similarities, component shifts, raw vectors, and a run manifest.

These prototype texts and results are **synthetic and non-evidential**. They demonstrate that the v3.4 data flow, mathematics, Azure connection, and output structure work correctly. They are not final theological findings and must not be presented as validated evidence about Catholic theology or the audited model.

The next substantive phase is a source-grounded five-audit pilot. Synthetic references will be replaced with short references derived from verified Catholic and disciplinary sources, followed by genuinely separate held-out validation, natural paraphrases, sensitivity analysis, review, and benchmark freeze.

> **For supervisors and reviewers:** Read the [full development log](DEVELOPMENT_LOG.md), especially the [detailed 12 July 2026 Step 1 record](DEVELOPMENT_LOG.md#step-1-2026-07-12), for the complete interactive design decisions, implementation history, mock and Azure tests, initial fixture-relative observations, limitations, documentation safeguards, and next-step plan.

### Development milestones

| Date | Milestone | Status | Detailed record |
|---|---|---|---|
| **12 July 2026** | Lean synthetic prototype, automated tests, mock run, and Azure `text-embedding-3-large` integration | **Complete** | [Full Step 1 record](DEVELOPMENT_LOG.md#step-1-2026-07-12) |
| **10 July 2026** | CTSB v3.4 methodology redesign and archival separation from v2 | **Complete** | [Methodology-redesign record](DEVELOPMENT_LOG.md#methodology-redesign-2026-07-10) |
| **Next phase** | Source-grounded and independently reviewed five-audit pilot | Planned | [Benchmark construction area](data/benchmarks/v3_4/README.md) |

### Primary Step 1 records

- [Audit definitions](data/benchmarks/v3_4/prototype/comparisons.csv)
- [Synthetic reference anchors](data/benchmarks/v3_4/prototype/references.csv)
- [Controlled contextual queries](data/benchmarks/v3_4/prototype/queries.csv)
- [Synthetic validation passages](data/benchmarks/v3_4/prototype/validation.csv)
- [Integrated Python prototype](scripts/ctsb_v3_4_prototype.py)
- [Automated tests](tests/test_ctsb_v3_4_prototype.py)
- [Full development log](DEVELOPMENT_LOG.md)

Generated mock and Azure prototype-run outputs remain local under `outputs/v3_4/prototype_runs/` and are intentionally excluded from Git.
<!-- END V3_4_CURRENT_STATUS -->

---

## 1. Project purpose

This project performs a black-box theological audit of a commercial text-embedding model.

Its purpose is not to use vector similarity to determine theological truth. It is to make the otherwise opaque semantic behaviour of an embedding system available for theological examination.

The project asks where Catholic theological meaning is:

- stably represented;
- foregrounded or attenuated under ambiguity;
- dependent on explicit context;
- jointly accessible with valid psychological, biological, clinical, legal, social, and ordinary-language dimensions;
- displaced by another semantic register;
- or difficult to recover in morally and pastorally critical contexts.

The intended contribution resembles a computational semantic autopsy. It exposes representational patterns that theologians cannot inspect by reading source code or by looking at an embedding vector directly.

A vector is only a numerical representation. The theological interpretation comes from controlled comparisons with source-grounded and independently reviewed natural-language references.

---

## 2. Direct object of study

The direct object of v3.4 is:

> Azure/OpenAI `text-embedding-3-large`

The study does not claim to audit:

- ChatGPT's hidden states;
- a GPT model's internal embedding layer;
- all OpenAI systems;
- all embedding models;
- all Christian traditions;
- or the truth of Catholic theology.

The project is specifically a Catholic theological case study of one deployed commercial embedding endpoint.

---

## 3. Why audit an embedding model?

Embeddings are independently deployed semantic infrastructure used in:

- semantic search;
- retrieval-augmented generation;
- document ranking;
- classification;
- clustering;
- recommendation;
- memory;
- routing;
- and content retrieval.

Users may not knowingly interact with an embedding model, but embeddings can affect which documents, concepts, or resources are selected for a user-facing AI system.

Embedding models are therefore not studied merely because they return convenient numbers. They are studied because they perform a real semantic function in contemporary AI systems.

Unlike a generative chatbot response, an embedding is normally stable under a fixed model version and configuration. This makes controlled semantic comparisons reproducible.

### Relationship to ChatGPT

`text-embedding-3-large` is not assumed to be ChatGPT's internal embedding module.

The connection is layered:

1. **Embedding representation:** how meanings are organised in the audited vector space.
2. **Retrieval and ranking:** how those representations may affect which materials reach a user-facing system.
3. **Generative behaviour:** how a GPT model formulates an actual answer.

v3.4 studies the first layer. Retrieval and controlled generative-model audits remain future work.

---

## 4. Research questions

### 4.1 Research problem

The project is not primarily asking whether adding words such as “Catholic,” “Christian,” or “theological” moves a query toward Catholic references. That effect is largely predictable and serves mainly as a diagnostic control.

The substantive problem is **theological adequacy under semantic competition**.

A model may recognise Catholic vocabulary while continuing to organise a concept primarily through another register—for example, autonomous choice, biological function, psychological wellbeing, legal status, clinical symptoms, romantic affect, economic value, or generic religious imagery.

This can produce **theological framing–content divergence**: a query or downstream system appears Catholic at the surface level while its substantive semantic organisation remains generic, reduced, displaced, or off-target.

The project does not attribute consciousness, belief, a subconscious, or deceptive intention to an embedding model. Appropriate terms include:

- default semantic tendency;
- latent representational prior;
- context-resistant register pull;
- residual comparison-register dominance;
- surface contextualisation without substantive theological recovery;
- theological framing–content divergence;
- and a possible downstream illusion of theological adequacy.

### 4.2 Primary research question

> **When morally significant, theologically ambiguous, or pastorally critical concepts are expressed in natural language—and when Catholic theological content is supplied either implicitly or explicitly—how reliably does Azure/OpenAI `text-embedding-3-large` preserve access to specifically Catholic theological meaning alongside named psychological, biological, clinical, legal, social, economic, affective, lexical, and generic-religious registers? Which concepts instead exhibit reduction, displacement, context-resistant comparison-register pull, generic-religious substitution, label dependence, persistent theological attenuation, or theological framing–content divergence?**

In simpler language:

> **When a user has not already supplied an obviously theological answer, what meaning does the model foreground? Even when Catholic framing is supplied, does the underlying semantic representation become substantively Catholic, or does another register continue to control it?**

### 4.3 RQ1 — Default semantic foregrounding

> **Under bare, natural-general, and genuinely ambiguous wording, which named semantic register does the model foreground for each concept?**

Examples include whether:

- freedom is organised primarily around autonomous choice or also around truth, goodness, responsibility, virtue, vocation, and final ends;
- grief is organised primarily around psychological bereavement or also retains Catholic-pastoral meaning;
- death is represented primarily as biological cessation or also retains dignity, judgment, resurrection, and hope;
- human dignity is narrowed to legal status;
- happiness is narrowed to subjective wellbeing;
- grace is treated mainly as elegance;
- and judgment after death is represented mainly through generic religious imagery.

Other registers are not presumed false. The question is whether one becomes disproportionately dominant or excludes dimensions necessary for theological interpretation.

### 4.4 RQ2 — Joint accessibility versus theological reduction

> **Can Catholic theological meaning and a valid adjacent register remain simultaneously accessible, or does contextualising one register suppress the other?**

Catholic theology does not deny biological, psychological, medical, legal, social, affective, or economic dimensions.

Examples include:

- whether biological death and eschatological meaning can coexist;
- whether grief can remain psychologically intelligible while retaining prayer, consolation, accompaniment, communion, and resurrection hope;
- whether disability can retain medical and functional description without losing intrinsic dignity and personhood;
- and whether palliative care can retain clinical competence together with moral and pastoral accompaniment.

The desired outcome is not necessarily Catholic dominance. For complementary or valid-but-partial relationships, **joint accessibility** may be the more appropriate behaviour.

### 4.5 RQ3 — Theological legibility without an overt label

> **Does substantive Catholic theological content become associated with source-grounded Catholic references when words such as “Catholic,” “Christian,” or “theology” are absent?**

This asks whether the model recognises theological substance rather than only an identity label.

For example:

> Human freedom reaches fulfilment when it is directed toward truth and the good.

If equivalent theological content remains weak until “In Catholic teaching” is added, the concept may exhibit **label dependence** rather than robust theological legibility.

### 4.6 RQ4 — Context-resistant register pull under Catholic framing

> **When substantive or explicit Catholic framing is supplied, do previously dominant comparison registers remain disproportionately influential?**

Possible cases include:

- Catholic freedom language remaining organised around unrestricted choice;
- Catholic euthanasia language remaining organised around autonomous assisted death;
- Catholic disability language remaining dominated by function or capacity;
- Catholic grief language remaining exclusively psychological;
- and Catholic particular judgment remaining indistinguishable from generic afterlife imagery.

High comparison similarity is not automatically defective. The question is whether Catholic meaning becomes sufficiently and robustly accessible for the registered theological relationship.

### 4.7 RQ5 — Theological framing–content divergence

> **Which concepts appear successfully Catholic-contextualised at the surface level while remaining comparatively weak, generic, displaced, or off-target relative to source-grounded Catholic content?**

Possible indicators include:

- explicit Catholic wording while Catholic-reference proximity remains comparatively weak;
- a comparison reference remaining locally dominant;
- generic-religious references outranking Catholic-specific references;
- positive $\Delta CAS$ without positive $\Delta S_C$;
- movement caused primarily by the label rather than equivalent theological content;
- disagreement between nearest-reference ranking and mean reference-field contrast;
- and persistence across paraphrases and reference-sensitivity checks.

This is the embedding-level form of a possible **illusion of theological adequacy**. Actual misleading chatbot answers or user trust would require downstream retrieval, generation, and user studies.

### 4.8 RQ6 — Genuine recovery versus apparent recovery

> **When a query moves relatively toward Catholic references, is that movement caused by actual Catholic-reference association gain or merely by movement away from another register?**

For matched contexts:

$$
\Delta CAS=\Delta S_C-\Delta S_R
$$

The analysis distinguishes:

- **genuine theological association gain:** $S_C$ increases;
- **joint enrichment:** both $S_C$ and $S_R$ remain substantial;
- **strong differentiation:** $S_C$ increases while $S_R$ decreases;
- **register displacement:** $S_R$ decreases while $S_C$ remains stable;
- **misleading relative recovery:** CAS increases while $S_C$ decreases;
- and **context resistance:** neither component changes materially.

A positive CAS shift must never automatically be described as Catholic activation or theological recovery.

### 4.9 RQ7 — Critical and crisis-context behaviour

> **When concepts are expressed through natural crisis, suffering, bereavement, suicidal distress, terminal illness, euthanasia requests, dying, or end-of-life care, does the model preserve clinically necessary meaning while retaining access to dignity, mercy, hope, accompaniment, prayer, moral seriousness, and pastoral care?**

Strong clinical or psychological association is not automatically a defect. In suicide-related language, it may be necessary for safety.

The nontrivial question is whether crisis wording permits joint clinical-pastoral accessibility or instead makes theological-pastoral meaning inaccessible.

### 4.10 RQ8 — Persistent theological attenuation

> **Which concepts remain comparatively weak in Catholic-reference proximity across natural, ambiguous, critical, integrative, label-free theological, and explicit Catholic conditions?**

The strongest warning cases would combine:

- weak theological accessibility in natural language;
- little gain from substantive theological content;
- continued comparison-register dominance under explicit Catholic framing;
- generic substitution rather than Catholic specificity;
- and stability across natural paraphrases, source-grounded reference alternatives, and leave-one-reference-out checks.

Such concepts may require particular caution in embedding-mediated theological search, retrieval, classification, or recommendation.

### 4.11 RQ9 — Recurring theological patterns

> **Are representational vulnerabilities concentrated in particular theological loci or theological relationship types?**

The principal hypotheses are:

- **teleological compression:** freedom, happiness, conscience, or virtue reduced to choice, wellbeing, preference, or behaviour;
- **anthropological narrowing:** personhood and dignity reduced to biology, function, capacity, law, or economics;
- **affective compression:** love, communion, marriage, or self-gift reduced to feeling, attraction, preference, or social attachment;
- **generic-religious substitution:** Catholic-specific doctrines represented through broad cultural-religious imagery;
- **critical-context attenuation:** theological-pastoral meaning becoming less accessible under crisis language;
- **label dependence:** Catholic vocabulary being recognised more reliably than Catholic theological substance;
- and **framing–content divergence:** Catholic surface framing without adequate Catholic semantic recovery.

These are hypotheses to test, not conclusions imported from v2 or assumed in advance.

### 4.12 RQ10 — Robustness, validation, and theological calibration

> **Which observed patterns survive genuinely independent validation, natural paraphrasing, leave-one-reference-out analysis, alternative source-grounded references, pre-assigned relationship interpretation, and theological or disciplinary review?**

A single negative CAS value is not sufficient to issue a theological warning.

Robust interpretation requires:

- source-grounded reference fields;
- genuinely separate held-out validation;
- successful Catholic and comparison recall;
- natural paraphrase stability;
- leave-one-reference-out stability;
- component-level shift analysis;
- appropriate nearest-reference rankings;
- review of the theological relationship between registers;
- and benchmark freeze before final model evaluation.

The intended outcome is a **calibration map for theologians**, not a universal Catholic score.

### 4.13 Evidential roles of the query conditions

The query conditions do not have equal evidential importance.

#### Primary substantive conditions

1. natural contemporary general use;
2. natural moral or pastoral ambiguity;
3. natural critical or crisis language;
4. integrative theological-proximate language.

These conditions address semantic foregrounding, competition, reduction, joint accessibility, and critical-context behaviour.

#### Substantive recovery condition

5. label-free theological content.

This tests whether theological substance is recoverable without an overt Catholic identity label.

#### Diagnostic controls

6. bare concept;
7. explicit Catholic framing.

The explicit Catholic condition is a positive contextualisation control and a secondary test of label dependence, residual register pull, and framing–content divergence.

“Adding Catholic wording increases Catholic association” is not a principal research finding by itself.

### 4.14 What the embedding audit can uniquely establish

If the final instrument is validated, it can establish benchmark-relative evidence concerning:

- which semantic register this specific embedding model foregrounds;
- which theological concepts remain legible without overt labels;
- whether theological and proximate meanings remain jointly accessible;
- whether Catholic framing produces substantive Catholic-reference recovery;
- whether apparent recovery is caused only by comparison-register suppression;
- whether generic religion substitutes for Catholic specificity;
- which concepts exhibit context-resistant tendencies;
- and which concepts may require caution in embedding-mediated theological retrieval.

These are empirical questions that cannot be answered merely by observing that words have multiple meanings.

### 4.15 Study boundary and downstream risk

The present direct object is the embedding layer.

The wider risk is layered:

1. **Embedding representation:** how semantic associations are organised.
2. **Retrieval and ranking:** which documents or concepts are selected.
3. **Generative response:** how a language model formulates an answer.
4. **User perception:** whether Catholic framing creates unwarranted trust.

CTSB directly tests the first layer and provides calibration for later layers.

It cannot by itself establish intentional deception, doctrinal error in an actual chatbot answer, or actual user misperception.

The central contribution is:

> **The project asks whether an AI embedding can appear appropriately Catholic through vocabulary and framing while its substantive semantic organisation remains reduced, generic, context-resistant, or dominated by another register—and it provides theologians with an empirical calibration map showing where theological meaning is robust, jointly accessible, fragile, label-dependent, or potentially misleading.**
## 5. Preliminary v2 findings to be re-tested

The v2 benchmark generated the following historical aggregate results:

| Context or shift | v2 mean | v2 bootstrap 95% interval |
|---|---:|---:|
| Bare CAS | -0.0202 | -0.0390 to -0.0022 |
| Ordinary CAS | +0.0234 | +0.0086 to +0.0373 |
| Academic CAS | +0.0525 | +0.0377 to +0.0667 |
| Explicit Catholic CAS | +0.1113 | +0.0986 to +0.1241 |
| Ordinary-to-Catholic shift | +0.0880 | +0.0773 to +0.0991 |

The Life and Death supplement produced:

| Context or shift | v2 mean | v2 bootstrap 95% interval |
|---|---:|---:|
| Bare CAS | -0.0438 | -0.0797 to -0.0095 |
| Ordinary CAS | -0.0069 | -0.0363 to +0.0202 |
| Academic CAS | +0.0104 | -0.0209 to +0.0398 |
| Explicit Catholic CAS | +0.0939 | +0.0657 to +0.1210 |
| Ordinary-to-Catholic shift | +0.1009 | +0.0782 to +0.1225 |

These are **archived exploratory findings**, not v3.4 results.

They motivate, but do not predetermine, the following v3.4 hypotheses:

1. The audited model is not uniformly dominated by non-theological registers.
2. Catholic-associated neighbourhoods appear present but vary substantially in accessibility.
3. Explicit Catholic wording produces a strong relative shift.
4. The shift may not always represent an increase in Catholic-reference similarity.
5. Theological fragility may be concentrated in morally, anthropologically, and pastorally ambiguous concepts.
6. Biological, clinical, psychological, legal, economic, affective, and autonomy-centred registers may be especially salient in some domains.
7. Crisis concepts such as grief, suicide, euthanasia, dying, and end-of-life care require separate critical-context analysis.

v3.4 will re-test these claims using source-grounded references, held-out validation, natural queries, explicit relationship metadata, and component-level analysis.

---

## 6. How the embedding comparison actually works

An embedding model does not output natural-language explanations. It returns a numerical vector.

For an exact text $q$, the model returns:

$$
e(q)=[x_1,x_2,\ldots,x_d]
$$

where $d$ is the model's embedding dimension.

There is no individual coordinate that means:

- Catholic;
- psychological;
- biological;
- moral;
- secular;
- or theological.

The method works by embedding **both the query and known reference texts**, then comparing their vectors.

### Example

Suppose the query is:

> Grief in Catholic theology.

The model embeds that query:

$$
e(q)
$$

The project also embeds source-grounded Catholic-pastoral reference texts, such as:

- mourning held in Christian hope;
- sorrow before God;
- consolation through prayer and communion;
- hope in the resurrection amid loss.

These become:

$$
e(c_1),e(c_2),\ldots,e(c_m)
$$

A separately defined psychological-bereavement reference set might include:

- emotional response to loss;
- bereavement;
- psychological sorrow;
- mourning process;
- coping with death.

These become:

$$
e(r_1),e(r_2),\ldots,e(r_n)
$$

The pipeline calculates cosine similarity between the query vector and every reference vector.

The natural-language reference texts are not decoded from the vectors. The project already knows which original text generated each stored vector.

A result table can therefore report the original text attached to the nearest reference vector.

“Top reference” means:

> top-ranked among the predefined benchmark references supplied for that concept.

It does not mean the globally nearest possible phrase in the model's entire semantic space.

---

## 7. Catholic Association Contrast

v3.4 uses the name:

> **Catholic Association Contrast (CAS)**

This replaces the older phrase “Catholic Alignment Score,” which could be confused with normative AI alignment.

For query $q$, Catholic reference set $C$, and comparison-register reference set $R$:

$$
S_C(q)=\frac{1}{|C|}\sum_{c\in C}\cos(e(q),e(c))
$$

$$
S_R(q)=\frac{1}{|R|}\sum_{r\in R}\cos(e(q),e(r))
$$

$$
CAS(q;C,R)=S_C(q)-S_R(q)
$$

Interpretation:

| Result | Meaning |
|---|---|
| $CAS>0$ | Catholic references are closer on average than the specified comparison references |
| $CAS<0$ | Comparison references are closer on average than the Catholic references |
| $CAS\approx0$ | Little relative separation between the two reference sets |
| $\Delta S_C>0$ | Mean similarity to Catholic references increased |
| $\Delta S_R<0$ | Mean similarity to the comparison register decreased |
| $\Delta CAS>0$ | Catholic references gained relative to the comparison references |

A negative CAS does not independently mean:

- common language;
- secular ideology;
- hostility to Catholic theology;
- absence of Catholic associations;
- or theological error.

It means only that the selected comparison references have greater mean cosine similarity than the selected Catholic references.

---

## 8. Methodological foundation

The CAS formula adapts the single-target differential cosine-association function introduced in the Word Embedding Association Test:

$$
s(w,A,B)= \mathrm{mean}_{a\in A}\cos(w,a) - \mathrm{mean}_{b\in B}\cos(w,b)
$$

Caliskan, Bryson, and Narayanan used this function within the wider WEAT procedure.

May et al. extended WEAT-style association testing to sentence encoders through SEAT. Their results also identified important cautions:

- sentence templates can influence results;
- reference sets may not form coherent concepts for an encoder;
- similar tests can produce inconsistent outcomes;
- cosine-based intrinsic effects may not predict downstream behaviour;
- and a null result does not prove absence of bias.

Tsirtsis et al. provide a contemporary 2026 example of reference-based cosine classification using modern embedding models, human-labelled texts, held-out calibration, model ensembles, and cross-format validation.

v3.4 borrows the foundational differential-association logic while adding theological source provenance, held-out validation, relationship typing, critical-context analysis, and decomposition of the component similarities.

### Methodological contribution

CTSB v3.4 proposes a domain-specific synthesis for Catholic theological auditing of embedding models. It combines peer-reviewed foundations in differential embedding association, controlled contextual contrast, minimal-pair evaluation, held-out validation, and sensitivity analysis with theological relationship typing, component-level shift decomposition, integrative-register analysis, and critical-context evaluation.

The individual computational techniques are established or strongly precedented. Their synthesis and theological operationalisation constitute this project's methodological contribution. CTSB v3.4 is not yet an independently peer-reviewed or universally validated instrument, and the project does not claim historical priority without a systematic literature review.

---

## 9. How a reference is identified as Catholic

The embedding model does not decide which reference texts are Catholic.

Catholic classification is established outside the model through:

1. identifiable Catholic sources;
2. careful natural-language extraction or paraphrase;
3. recorded source provenance;
4. independent theological review;
5. and held-out validation.

Potential sources include:

- the *Catechism of the Catholic Church*;
- conciliar documents;
- papal encyclicals;
- doctrinal texts;
- Catholic social teaching;
- authoritative Catholic moral and pastoral documents.

The correct empirical statement is not:

> The vector itself is Catholic.

It is:

> The query has greater mean cosine similarity to vectors generated from source-grounded and independently reviewed Catholic reference texts.

---

## 10. Held-out validation

Reference review alone is insufficient.

v3.4 must test the numerical instrument using natural-language passages not used to construct the references.

### Stage A: clear-register validation

Create separate held-out texts that independent reviewers classify as:

- clearly Catholic-theological in the relevant sense; or
- clearly representative of the specified comparison register.

The audit then tests whether CAS distinguishes those held-out texts.

Primary validation measures:

- balanced accuracy;
- Catholic-reference recall;
- comparison-register recall;
- macro F1;
- confusion matrix.

If the instrument cannot distinguish clear held-out examples, ambiguous-query results for that concept should not receive strong interpretation.

### Stage B: integrative passages

Some texts legitimately combine theological and other dimensions.

For example:

> Grief is a profound psychological response to bereavement that, in Christian life, is held within prayer and hope in the resurrection.

Such a passage should not be forced into an exclusive Catholic-versus-psychological class.

Instead, v3.4 examines the pair:

$$
(S_C,S_R)
$$

and asks whether both registers remain accessible.

### Stage C: critical and crisis-language passages

Natural critical-context texts will test concepts such as:

- grief;
- suicide;
- euthanasia;
- suffering;
- dying;
- end-of-life care.

These passages require ethical and theological review before evaluation.

---

## 11. Theological relationships between registers

Catholic, psychological, biological, medical, legal, social, and ordinary meanings are analytically distinguishable but not always mutually exclusive.

Before any final embedding run, each concept-level comparison must be assigned one relationship type.

| Relationship type | Example | Interpretation |
|---|---|---|
| Complementary levels | biological death and eschatological death | Both may describe the same reality at different explanatory levels |
| Valid but partial | grief as bereavement | The comparison meaning may be valid but incomplete if treated as exhaustive |
| Normatively conflicting | direct euthanasia as permissible versus Catholic moral rejection | The propositions genuinely differ morally |
| Alternative lexical senses | grace as divine gift versus elegance | Competing senses of one expression |
| Generic religious versus Catholic-specific | generic afterlife judgment versus particular judgment | Both are religious, but one is more doctrinally specific |

This theological relationship must be established before viewing model results.

The model's numerical output must not determine retrospectively whether the comparison register is compatible or incompatible with Catholic theology.

---

## 12. Shift decomposition

For matched contexts $q_0$ and $q_1$:

$$
\Delta CAS=CAS(q_1)-CAS(q_0)
$$

Because:

$$
CAS=S_C-S_R
$$

it follows exactly that:

$$
\Delta CAS=\Delta S_C-\Delta S_R
$$

This distinguishes several semantic behaviours.

| Change | Interpretation |
|---|---|
| $S_C$ increases while $S_R$ is stable | Theological association gain |
| Both increase, with greater Catholic gain | Joint accessibility with theological enrichment |
| $S_C$ increases and $S_R$ decreases | Strong register differentiation |
| $S_C$ is stable while $S_R$ decreases | Relative Catholic shift without theological gain |
| $S_C$ decreases but $S_R$ decreases more | Positive CAS shift despite declining Catholic proximity |
| Neither changes materially | Context resistance |

A positive CAS shift must not automatically be called “Catholic activation.”

A claim of theological association gain requires:

- positive $\Delta S_C$;
- stability across natural paraphrases;
- reference-sensitivity checks;
- compatibility with held-out validation;
- and appropriate nearest-reference results.

---

## 13. Theological behaviour taxonomy

The final v3.4 analysis will classify observed behaviour more precisely than positive or negative CAS.

| Behaviour type | Operational meaning |
|---|---|
| Stable theological legibility | Catholic-reference association remains strong across relevant contexts |
| General-use foregrounding with theological recoverability | Another register dominates initially, but Catholic association rises robustly under context |
| Joint accessibility | Catholic and valid comparison-register similarities remain simultaneously substantial |
| Theological association gain | Catholic similarity itself increases |
| Register displacement | Relative Catholic movement is driven mainly by suppression of another register |
| Label-dependent shift | Overt religious wording produces substantially more movement than equivalent theological content |
| Persistent theological attenuation | Catholic-reference proximity remains comparatively weak across reviewed contexts |
| Mixed local/global association | The top-ranked reference and mean reference-field contrast point in different directions |

This taxonomy is intended to help theologians inspect where AI behaviour warrants particular caution.

---

## 14. Theological loci retained from v2

### 14.1 Freedom, truth, and moral teleology

v3.4 tests possible **teleological compression**.

The question is whether concepts such as:

- freedom;
- happiness;
- flourishing;
- responsibility;
- conscience;
- autonomy;
- rights;
- virtue;
- obedience;
- and license

are represented mainly through choice, permission, self-expression, liability, or psychological outcome, while orientation toward truth, goodness, virtue, vocation, and final ends remains comparatively attenuated.

The v2 findings for autonomy, happiness, flourishing, responsibility, freedom, and license remain preliminary cases for re-testing.

### 14.2 Human dignity and theological anthropology

v3.4 tests possible **anthropological narrowing**.

The question is whether body, personhood, disability, poverty, work, suffering, and death are organised primarily through material, functional, legal, economic, or biological descriptions, or whether their theological-anthropological significance remains jointly accessible.

Relevant Catholic dimensions include:

- createdness;
- intrinsic dignity;
- embodied personhood;
- body-soul unity;
- relational vocation;
- communion;
- moral agency;
- and final destiny.

The proximate descriptions are not presumed false. The empirical question is whether one dimension dominates or excludes another.

### 14.3 Love, communion, and sacramentality

v3.4 examines whether affective, romantic, bodily, social, charitable, and sacramental dimensions can remain semantically integrated.

It re-tests v2 patterns involving:

- love;
- friendship;
- neighbour;
- sexuality;
- marriage;
- family;
- chastity;
- self-gift;
- caritas;
- communion;
- and sacramentality.

The research does not oppose eros to agape or affection to Catholic love. It asks whether Catholic contextualisation expands the semantic field or merely substitutes one vocabulary for another.

### 14.4 Sin, grace, and redemption

This locus functions partly as an internal theological control.

It compares explicitly religious concepts such as:

- salvation;
- sanctification;
- grace;
- original sin;
- sacrament;
- and resurrection

with adjacent moral and pastoral concepts such as:

- guilt;
- shame;
- forgiveness;
- justification;
- reconciliation;
- and judgment.

The v2 result suggested that theological legibility may be strongest where religious meaning is lexically explicit and weaker where theological interpretation operates through ordinary human experience.

v3.4 will test that proposition rather than assume it.

---

## 15. Life and Death critical-context module

Life and death will remain a central v3.4 module.

The research question is:

> **How does the embedding reorganise semantic salience when life, death, grief, suffering, suicide, euthanasia, and dying are expressed as natural existential, pastoral, or crisis-language utterances rather than abstract concepts?**

Possible behaviours include:

- crisis-register dominance;
- preservation of clinically necessary meaning;
- theological attenuation;
- joint clinical-pastoral accessibility;
- context-dependent theological recovery;
- persistent attenuation;
- and register displacement.

Strong crisis or mental-health associations are not automatically classified as defects. For suicide, such associations may be appropriate and safety-relevant.

The theological question is whether the model also retains access to concepts such as:

- dignity;
- mercy;
- accompaniment;
- hope;
- moral seriousness;
- prayer;
- resurrection;
- and pastoral care.

---

## 16. Planned query conditions

The exact wording must be developed, reviewed, and frozen before the final run.

The planned conditions are:

1. **Bare or minimally specified concept**
2. **Natural contemporary general-use context**
3. **Natural morally or pastorally ambiguous context**
4. **Natural critical or crisis context**, where appropriate
5. **Label-free theological-content context**
6. **Explicit Catholic contextualisation**
7. **Integrative theological-proximate context**, for complementary domains

Not every condition is appropriate for every concept.

The benchmark protocol must specify applicability before evaluation.

---

## 17. Minimum robustness requirements

v3.4 prioritises a small set of foundational checks.

### Required

1. Held-out validation of clear-register texts
2. Independent theological review of Catholic references
3. Recorded source provenance
4. Leave-one-reference-out sensitivity
5. Natural paraphrase or leave-one-template-out sensitivity
6. Component-level shift decomposition
7. Small embedding determinism check
8. Full query-to-reference cosine export
9. Frozen benchmark before final evaluation

### Statistical unit

The principal statistical unit remains the concept.

Multiple references and query paraphrases improve measurement reliability but must not be treated as fully independent conceptual observations.

### Primary statistical summaries

- mean concept-level shift;
- median concept-level shift;
- bootstrap confidence interval over concepts;
- number and proportion of positive shifts;
- paired sign-flip permutation test;
- held-out balanced accuracy;
- class-specific recall;
- macro F1;
- confusion matrix.

Subgroup and concept-type analyses will be marked exploratory unless pre-specified and adequately powered.

---

## 18. Raw and processed data

v3.4 will distinguish several data levels.

| Level | Content |
|---|---|
| Benchmark source data | Queries, references, provenance, relationship types, reviewer status, and data splits |
| Raw model output | High-dimensional embedding vectors |
| Descriptor-level scored data | Every query-to-reference cosine similarity and rank |
| Query-level summary | $S_C$, $S_R$, CAS, nearest references, and ranks |
| Concept-level summary | Context means and component-level shifts |
| Statistical summary | Validation metrics, confidence intervals, paired tests, and sensitivity results |

The descriptor-level export is essential because it allows reviewers to reconstruct every mean, contrast, and ranking.

---

## 19. Data before visualisation

The primary evidence is numerical analysis in the model's original high-dimensional embedding space.

Substantive conclusions will rely on:

- query-to-reference cosine similarities;
- component means;
- CAS;
- component-level shifts;
- held-out validation;
- confidence intervals;
- directional consistency;
- and robustness checks.

Visualisations remain important for:

- identifying heterogeneity;
- inspecting outliers;
- communicating behaviour types;
- and diagnosing misleading aggregates.

UMAP, if retained, will be explicitly exploratory. Its axes and apparent global distances will not be treated as substantive theological evidence.

The appropriate principle is:

> Numerical analysis establishes the result; visualisation diagnoses and communicates it.

---

## 20. What v3.4 may conclude

If validation succeeds, v3.4 may support benchmark-relative claims about:

- which semantic register is foregrounded under ambiguity;
- whether Catholic-reference proximity increases under context;
- whether theological and proximate dimensions remain jointly accessible;
- whether a relative shift is driven by enrichment or displacement;
- whether critical wording attenuates theological-pastoral association;
- and where persistent theological attenuation occurs.

It will not establish:

- machine belief;
- metaphysical ontology;
- theological truth;
- hostility toward Catholicism;
- behaviour of all embedding models;
- or ChatGPT's actual generated pastoral responses.

---

## 21. Relevance to theologians

The project translates vector-space behaviour into theological questions concerning:

- teleology;
- theological anthropology;
- reductionism;
- doctrinal legibility;
- moral ambiguity;
- semantic integration;
- pastoral adequacy;
- and critical-context vulnerability.

Its purpose is to help theologians say:

- where an AI model's theological associations are stable;
- where they are dependent on context;
- where valid clinical or psychological meanings dominate;
- where theological meaning is added without suppressing those meanings;
- where one register replaces another;
- and where particular caution is warranted.

The embedding model does not perform the theological interpretation. The audit provides empirical evidence that theologians can interpret.

---

## 22. Future enhancements

After the v3.4 methodology and benchmark are validated and frozen, future work may include:

1. cross-provider replication using a Google embedding model;
2. evaluation with three or more independent embedding families;
3. retrieval and ranking audits;
4. controlled generative GPT audits;
5. integrated RAG-system evaluation;
6. multilingual theological benchmarks;
7. other Christian or religious traditions;
8. multimodal theological representation.

Raw CAS values from different embedding models must not be compared as if they shared one calibrated scale.

For example:

> OpenAI CAS = 0.10 and Google CAS = 0.05

would not establish that OpenAI is twice as Catholic-associated.

Cross-model comparison should instead examine:

- held-out performance;
- within-model effect patterns;
- sign and direction consistency;
- class-specific recall;
- concept-level rank correlation;
- and standardised within-model effects.

---

## 23. Key methodological references

### Foundational differential association

Caliskan, A., Bryson, J. J., and Narayanan, A. (2017). “Semantics derived automatically from language corpora contain human-like biases.” *Science*, 356(6334), 183–186.  
https://doi.org/10.1126/science.aal4230

### Sentence-encoder extension and cautions

May, C., Wang, A., Bordia, S., Bowman, S. R., and Rudinger, R. (2019). “On Measuring Social Biases in Sentence Encoders.” *Proceedings of NAACL-HLT 2019*.  
https://aclanthology.org/N19-1063/

### Contemporary reference-based embedding validation

Tsirtsis, S., Rawal, K., Russell, C., Mittelstadt, B., and Wachter, S. (2026). “AI-Mediated Communication Can Steer Collective Opinion.” arXiv:2605.16245. Accepted for presentation at the AI4Good and Technical AI Governance Research workshops at ICML 2026.  
https://arxiv.org/abs/2605.16245

---

## 24. Current implementation status

The repository contains:

- the CTSB v3.4 methodology and synthetic five-audit prototype;
- the working v3.4 scoring engine;
- the generated CTSB v3.5-alpha 100-concept expansion;
- mock analysis and robustness support;
- and successful prior Azure integration with `text-embedding-3-large`.

The repository does not yet contain:

- a source-verified final v3.5 benchmark;
- genuinely independent held-out alpha validation;
- completed theological or disciplinary review;
- a frozen final 100-concept benchmark;
- final evidential v3.5 results;
- or a v3.5 dashboard.

The generated alpha must not be presented as a final benchmark. Archived v2 code and categories remain historical only.
## 25. Repository layout

    vector-space-theological-meaning/
    ├── README.md
    ├── VERSION
    ├── DEVELOPMENT_LOG.md
    ├── docs/
    │   ├── AI_HANDOFF_V3_4.md
    │   ├── AI_HANDOFF_V3_5_ALPHA.md
    │   ├── AI_HANDOFF_V3_5_BETA.md
    │   ├── CTSB_V3_5_ALPHA_PROTOCOL.md
    │   └── CTSB_V3_5_BETA_PLAN.md
    ├── data/
    │   └── benchmarks/
    │       ├── v3_4/
    │       │   └── prototype/
    │       └── v3_5_alpha/
    │           └── generated_100/
    ├── scripts/
    │   ├── ctsb_v3_4_prototype.py
    │   └── ctsb_v3_5_alpha.py
    ├── tests/
    │   ├── test_ctsb_v3_4_prototype.py
    │   └── test_ctsb_v3_5_alpha.py
    └── tools/
        └── build_ai_context.sh

Generated vectors, embedding caches, run outputs, context bundles, and backups remain local and are excluded from Git.
