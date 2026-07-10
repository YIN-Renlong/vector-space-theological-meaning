# Vector Space and Theological Meaning

## CTSB v3.4 Methodology Design

**From doctrinal legibility to theological behaviour under ambiguity and critical contexts**

CTSB v3.4 redesigns the project as a source-grounded and validated theological audit of Azure/OpenAI `text-embedding-3-large`.

The active repository currently contains the **v3.4 methodology protocol and benchmark-construction plan only**. The v3.4 benchmark data, audit script, statistical outputs, and dashboard have not yet been implemented.

The previous v2 implementation has been frozen in the repository archive:

- [CTSB-100 v2 context-draft archive](archive/ctsb_100_v2_context_draft/README.md)
- [CTSB-100 v1 draft archive](archive/ctsb_100_v1_draft/README.md)

Public archival dashboards:

- [CTSB-100 v2 dashboard](https://yin-renlong.github.io/vector-space-theological-meaning/archive/ctsb_100_v2_context_draft/index_v2_dashboard.html)
- [Life and Death v1 dashboard](https://yin-renlong.github.io/vector-space-theological-meaning/archive/ctsb_100_v2_context_draft/life_death_v1_dashboard.html)

The root `index.html` and `life_death.html` remain temporarily as compatibility copies of the v2 dashboards. They are not v3.4 results.

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

## 4. Primary research question

> **In morally ambiguous and pastorally critical concepts, how does Azure/OpenAI `text-embedding-3-large` distribute semantic salience among Catholic theological and valid psychological, biological, clinical, legal, social, economic, affective, generic-religious, and ordinary-language registers, and which recurring modes of behaviour—joint accessibility, theological association gain, register displacement, label dependence, context-dependent recovery, or persistent theological attenuation—appear across theological domains?**

This question is not answered by observing that words have several meanings.

The empirical questions concern a particular AI system:

- Which register is foregrounded under ambiguous wording?
- Does natural crisis wording reorganise the semantic field?
- Does Catholic contextualisation increase actual Catholic-reference proximity?
- Does a positive relative shift instead arise from movement away from another register?
- Can theological and clinically or psychologically valid dimensions remain simultaneously accessible?
- Which concepts remain comparatively attenuated across contexts?
- Are these patterns concentrated in particular theological loci?

---

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
s(w,A,B)=
\operatorname{mean}_{a\in A}\cos(w,a)
-
\operatorname{mean}_{b\in B}\cos(w,b)
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

The active v3.4 repository does not yet contain:

- a final v3.4 benchmark;
- a v3.4 audit script;
- v3.4 embedding results;
- or a v3.4 dashboard.

Those components will be implemented only after the written methodology, source procedure, review process, validation split, query conditions, and statistical plan are frozen.

The archived v2 code must not be silently reused as if it implemented the v3.4 protocol.

---

## 25. Repository layout

    vector-space-theological-meaning/
    ├── README.md
    ├── VERSION
    ├── docs/
    │   └── development_log.md
    ├── data/
    │   └── benchmarks/
    │       └── v3_4/
    │           └── README.md
    ├── archive/
    │   ├── ctsb_100_v1_draft/
    │   └── ctsb_100_v2_context_draft/
    ├── index.html
    └── life_death.html

The root HTML files are temporary compatibility copies of the v2 dashboards. Canonical historical copies are stored inside the v2 archive.
