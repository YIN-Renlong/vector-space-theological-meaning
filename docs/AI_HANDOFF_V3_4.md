# AI Handoff: CTSB v3.4

> **Status notice — 13 July 2026:** This document preserves the CTSB v3.4 Step 1 handoff. The active generated exploratory expansion is [CTSB v3.5-alpha](AI_HANDOFF_V3_5_ALPHA.md). CTSB v3.4 remains the mathematical and methodological foundation.

## Continuation instruction

You are continuing the project **Vector Space and Theological Meaning**.

Before proposing changes:

1. read the active root [README](../README.md);
2. read this handoff;
3. treat CTSB v3.4 as the controlling methodology;
4. treat the archived v1 and v2 files as historical evidence only;
5. do not silently restore the v2 “Catholic versus secular/common-language” design;
6. do not interpret synthetic prototype outputs as theological evidence;
7. do not begin dashboard work before the numerical instrument and benchmark are stable.

The immediate substantive task is **CTSB v3.4 Step 2: construct and evaluate a source-grounded five-audit pilot before expanding to a full benchmark**.

---

## 1. Project identity

- **Project:** Vector Space and Theological Meaning
- **Active methodology:** CTSB v3.4
- **Current implementation stage:** Step 1 complete; Step 2 pending
- **Direct object of study:** Azure/OpenAI `text-embedding-3-large`
- **Confirmed Azure vector dimensions:** 3,072
- **Primary orientation:** Catholic theological audit of embedding behaviour under ambiguity, multiple semantic registers, and morally or pastorally critical contexts
- **Current version marker:** `3.4-step1-complete`

The project is a black-box audit of a commercial embedding endpoint. It is not a test of theological truth, machine belief, ChatGPT hidden states, or all OpenAI systems.

---

## 2. Controlling documentation

Use this priority order:

1. [README.md](../README.md) — active methodology and public project account
2. [AI_HANDOFF_V3_4.md](AI_HANDOFF_V3_4.md) — current implementation state and next action
3. [DEVELOPMENT_LOG.md](../DEVELOPMENT_LOG.md) — detailed chronological research record
4. [v3.4 benchmark README](../data/benchmarks/v3_4/README.md) — benchmark-construction rules
5. Active prototype data, code, and tests
6. Archived v2 materials — historical reference only

The old location `docs/development_log.md` is only a compatibility link to the root development log.

Superseded handoffs are preserved in `docs/handoff_archive/` but are not active specifications.

---

## 3. Methodological contribution

CTSB v3.4 is a project-specific Catholic theological synthesis with peer-reviewed scientific foundations.

It combines:

- differential cosine association from WEAT-style methods;
- sentence-encoder cautions associated with SEAT;
- reference-based semantic comparison;
- controlled contextual contrasts;
- minimal-pair label perturbation;
- behavioural and contrast-set testing;
- held-out validation;
- component-level shift decomposition;
- and sensitivity analysis.

Its domain-specific contribution is the combination of those methods with:

- explicitly named comparison registers;
- pre-assigned theological relationship types;
- label-free theological and explicit Catholic conditions;
- integrative-register analysis;
- critical-context evaluation;
- and a theological behaviour taxonomy.

The method is original as a project-specific synthesis and theological operationalisation. It is not yet an independently peer-reviewed or universally validated instrument. Do not claim historical priority without a systematic literature review.

---

## 4. Mathematical instrument

For query text $q$, Catholic reference set $C$, and a specifically named comparison-register set $R$:

$$
S_C(q)=\frac{1}{|C|}\sum_{c\in C}\cos(e(q),e(c))
$$

$$
S_R(q)=\frac{1}{|R|}\sum_{r\in R}\cos(e(q),e(r))
$$

$$
CAS(q;C,R)=S_C(q)-S_R(q)
$$

CAS means **Catholic Association Contrast**, not Catholic Alignment Score.

Interpretation is relative:

- positive CAS: Catholic references are closer on average than the specified comparison references;
- negative CAS: comparison references are closer on average;
- CAS near zero: little separation between the two reference fields.

A negative value does not independently mean secularism, hostility, error, or absence of Catholic association.

For a registered baseline query $q_0$ and target query $q_1$:

$$
\Delta CAS=CAS(q_1)-CAS(q_0)
$$

and exactly:

$$
\Delta CAS=\Delta S_C-\Delta S_R
$$

A positive CAS shift does not by itself prove theological association gain. That claim requires positive $\Delta S_C$ as well as robustness and validation.

---

## 5. Theological relationship types

Every concept-to-register comparison must receive one relationship type before model results are examined:

1. `complementary_levels`
2. `valid_but_partial`
3. `normatively_conflicting`
4. `alternative_lexical_senses`
5. `generic_religious_vs_catholic_specific`

These relationships prevent every non-Catholic register from being treated as false or hostile.

Examples:

- biological death and eschatological death: complementary levels;
- grief as psychological bereavement: valid but partial;
- permissive euthanasia and Catholic moral rejection: normatively conflicting;
- grace as divine gift and grace as elegance: alternative lexical senses;
- generic afterlife judgment and particular judgment: generic religious versus Catholic-specific.

---

## 6. Query conditions

The active methodology permits:

1. bare or minimally specified concept;
2. natural contemporary general use;
3. natural morally or pastorally ambiguous context;
4. natural critical or crisis context, where appropriate;
5. label-free theological content;
6. explicit Catholic contextualisation;
7. integrative theological-proximate context.

Not every condition is appropriate for every concept.

Important analytical contrasts include:

- general to ambiguous;
- general to critical;
- general to label-free theological;
- label-free theological to explicit Catholic;
- general or critical to integrative;
- and stability across all applicable contexts.

A label-dependence test should be a genuine minimal pair wherever possible: the explicit Catholic query should differ from the label-free theological query mainly by the Catholic label, not by additional doctrinal content.

---

## 7. Step 1 completed on 12 July 2026

Step 1 produced a lean, non-evidential development prototype.

### Active tracked files

- [comparisons.csv](../data/benchmarks/v3_4/prototype/comparisons.csv)
- [references.csv](../data/benchmarks/v3_4/prototype/references.csv)
- [queries.csv](../data/benchmarks/v3_4/prototype/queries.csv)
- [validation.csv](../data/benchmarks/v3_4/prototype/validation.csv)
- [ctsb_v3_4_prototype.py](../scripts/ctsb_v3_4_prototype.py)
- [test_ctsb_v3_4_prototype.py](../tests/test_ctsb_v3_4_prototype.py)

### Prototype size

- 5 audit units
- 30 references
- 32 queries
- 28 validation passages
- 20 clear-register validation passages
- 90 unique embedded texts in the Azure fixture run

### Five audit units

| Audit ID | Concept | Comparison register | Relationship |
|---|---|---|---|
| `death_biological` | death | biological description | complementary levels |
| `grief_psychological` | grief | psychological bereavement | valid but partial |
| `euthanasia_assisted_dying` | euthanasia | permissive assisted dying | normatively conflicting |
| `grace_lexical` | grace | elegance and social charm | alternative lexical senses |
| `judgment_after_death_generic` | judgment after death | generic religious afterlife judgment | generic religious versus Catholic-specific |

Life and Death is integrated into the unified benchmark through the `life_death_module` field. It is no longer a separate computational pipeline.

---

## 8. Lean data design

The prototype deliberately uses four CSV files rather than a production-scale database.

### `comparisons.csv`

Defines one audit unit as:

> concept × specifically named comparison register

It records the locus, Life and Death flag, relationship type, critical-context applicability, rationale, and status.

### `references.csv`

Contains Catholic and comparison reference anchors.

It retains:

- reference ID;
- audit ID;
- group;
- exact text;
- source title;
- source location;
- text status;
- review status;
- notes.

The present anchors are synthetic fixtures. Final references must be source-grounded.

### `queries.csv`

Contains exact model inputs and explicit matched-query links.

The `baseline_query_id` and `contrast_type` fields prevent the analysis script from guessing which queries belong in a shift comparison.

### `validation.csv`

Contains separate clear-register, integrative, and critical passages.

Clear-register passages receive Catholic or comparison labels. Integrative and critical passages are scored through $(S_C,S_R,CAS)$ without being forced into an inappropriate exclusive class.

---

## 9. Integrated Python prototype

The active code is one integrated script:

`../scripts/ctsb_v3_4_prototype.py`

This was chosen deliberately to avoid over-engineering the prototype.

It supports:

- fixture creation;
- CSV validation;
- deterministic mock embeddings;
- Azure embedding calls;
- caching;
- full query-to-reference cosine export;
- reference ranking;
- $S_C$, $S_R$, and CAS;
- matched shifts;
- decomposition verification;
- synthetic held-out scoring;
- basic validation metrics;
- raw vector export;
- file hashes;
- and run manifests.

The active test file contains five passing tests:

1. fixture schema and ID links;
2. rejection of synthetic sources in final benchmark mode;
3. deterministic mock repeatability;
4. cosine identity;
5. full mock-pipeline execution and output reconstruction.

Do not split the script into many modules unless actual maintenance complexity later justifies it.

---

## 10. Step 1 runs

### Mock run

A deterministic local run verified the code path without contacting Azure.

Local run ID:

`fixture_mock_20260712-222901`

### Azure run

A successful Azure integration run used:

- provider: Azure OpenAI;
- deployment: `text-embedding-3-large-prova1`;
- Azure-reported model: `text-embedding-3-large`;
- API version: `2024-02-01`;
- dimensions: 3,072;
- 90 new embeddings;
- two API batches.

Local run ID:

`fixture_azure_20260712-223931`

Generated outputs are stored locally under:

`outputs/v3_4/prototype_runs/`

These outputs and the embedding cache are intentionally ignored by Git and excluded from the default AI context bundle.

The local `.env` was completed with the deployment and API-version variables, but `.env` must never be printed, bundled, or committed.

---

## 11. Step 1 technical verification

The following succeeded:

- Azure authentication;
- deployment access;
- batch embedding;
- 3,072-dimensional vector receipt;
- cache writing;
- full cosine export;
- query scoring;
- reference ranking;
- validation scoring;
- shift export;
- vector export;
- run-manifest creation;
- and numerical decomposition verification.

The maximum recorded shift-decomposition identity error was approximately:

$$
2.78\times10^{-17}
$$

This is ordinary floating-point precision.

Synthetic clear-register validation produced balanced accuracy and macro F1 of 1.0. This is only a pipeline sanity check because the fixture references and validation passages were authored together, are intentionally clear, and contain conceptual or lexical overlap.

---

## 12. Initial synthetic fixture observations

These observations demonstrate what the v3.4 analysis can distinguish. They are not final model findings.

### General to label-free theological content

| Audit | $\Delta S_C$ | $\Delta S_R$ | $\Delta CAS$ |
|---|---:|---:|---:|
| Death | +0.4107 | −0.2859 | +0.6966 |
| Grief | +0.3231 | −0.1082 | +0.4313 |
| Euthanasia | +0.2931 | −0.1430 | +0.4361 |
| Grace | +0.4467 | −0.4439 | +0.8906 |
| Judgment after death | +0.1969 | −0.1553 | +0.3522 |

All five fixture cases combined theological association gain with comparison-register reduction.

### Label-free theological to explicit Catholic

| Audit | $\Delta S_C$ | $\Delta S_R$ | $\Delta CAS$ |
|---|---:|---:|---:|
| Death | −0.0810 | −0.0229 | −0.0581 |
| Grief | −0.0351 | −0.0198 | −0.0153 |
| Euthanasia | −0.0330 | −0.0483 | +0.0153 |
| Grace | −0.0213 | +0.0997 | −0.1210 |
| Judgment after death | −0.0253 | −0.0521 | +0.0268 |

Adding the Catholic label did not increase $S_C$ in any fixture case. The two slightly positive CAS movements came from larger reductions in $S_R$, not theological gain.

This demonstrates the need to distinguish theological content from overt labelling. It does not establish a general property of the model.

### Critical contexts

- grief critical wording reduced $S_C$ and made CAS more negative;
- euthanasia produced a positive relative CAS shift even though $S_C$ declined, because $S_R$ declined more;
- death critical wording increased $S_C$ while biological similarity fell substantially.

The euthanasia fixture is the clearest example of relative shift without theological gain.

### Integrative contexts

- grief increased both $S_C$ and $S_R$, demonstrating a prototype pattern of joint accessibility with theological enrichment;
- death and euthanasia increased $S_C$ while decreasing $S_R$, suggesting differentiation rather than simple joint enrichment;
- judgment after death changed $S_C$ little while reducing generic-religious similarity.

An integrative query must therefore be evaluated through both component scores.

### Mixed local/global association

Several fixture queries showed disagreement between:

- the sign of mean-field CAS;
- and the group of the single nearest reference.

This confirms the value of preserving nearest-reference rankings alongside mean reference-field contrasts.

---

## 13. Source policy

Queries are controlled experimental inputs and do not require citations merely because they are short authored sentences.

Reference anchors have a different function: they define the benchmark-relative Catholic and comparison fields.

For the final empirical benchmark:

- Catholic references should derive from identifiable Catholic sources;
- comparison references should derive from appropriate disciplinary, lexical, legal, scientific, or religious-studies sources;
- direct quotation, close paraphrase, and researcher summary must be distinguished;
- provenance and review must remain attached to each reference.

Likely Catholic source classes include:

- the *Catechism of the Catholic Church*;
- conciliar documents;
- papal encyclicals;
- DDF/CDF doctrinal texts;
- official moral and pastoral documents;
- Catholic social teaching;
- official liturgical texts;
- and canon law where relevant.

Real source collection was intentionally deferred until after the code prototype succeeded.

---

## 14. v2 status

The main v2 benchmark tested:

- 100 concepts;
- 1,000 queries;
- four query contexts;
- five Catholic descriptors per concept;
- and five broad “secular/common-language” descriptors per concept.

The Life and Death supplement tested 24 concepts and 240 queries.

These are archived exploratory results. They motivate hypotheses and concept selection but are not copied into v3.4.

The broad v2 comparison group mixed ordinary, psychological, biological, clinical, legal, social, economic, and generic-religious meanings. v3.4 replaces it with explicitly named comparison registers and pre-assigned relationship metadata.

Current v3.4 code already exists, so legacy v2 code is no longer necessary in every new-thread context bundle.

---

## 15. Output and evidence policy

The standard data levels remain:

1. benchmark source data;
2. raw model vectors;
3. reference-level cosine data;
4. query-level $S_C$, $S_R$, CAS, and ranks;
5. concept/context summaries;
6. shift decomposition;
7. validation;
8. sensitivity;
9. statistical summaries.

Numerical high-dimensional analysis establishes results.

Visualisation is secondary and must not determine substantive conclusions. UMAP, if later retained, is exploratory only.

The root `index.html` and `life_death.html` remain compatibility copies of v2 dashboards. They are not v3.4 results.

---

## 16. Immediate next step: source-grounded five-audit pilot

Do not expand immediately to 100 concepts.

Step 2 should keep the current five audit units and:

1. identify authoritative Catholic sources for each Catholic reference field;
2. identify suitable disciplinary or lexical sources for each comparison field;
3. write short source-grounded reference statements;
4. retain quotation/paraphrase/summary status;
5. create genuinely separate held-out validation passages;
6. tighten label-free and explicit-Catholic pairs into true minimal pairs;
7. add two or three natural paraphrases for important conditions;
8. add leave-one-reference-out sensitivity;
9. add paraphrase or leave-one-template-out sensitivity;
10. define validation acceptance criteria before viewing ambiguous-query results;
11. obtain appropriate theological and disciplinary review;
12. freeze the five-audit pilot;
13. run Azure;
14. inspect validation and robustness;
15. only then decide how broadly to scale the benchmark.

The current integrated script can read revised CSV files. It does not need to be replaced merely because the fixture texts change.

---

## 17. Claims permitted after Step 1

Step 1 supports only implementation claims:

- the lean data model works;
- the Python engine works;
- Azure integration works;
- the endpoint returned the expected model family and vector size;
- full reference-level scoring works;
- CAS reconstruction works;
- matched shifts work;
- and decomposition is exact within floating-point precision.

Step 1 does not support final claims about:

- theological legibility;
- label dependence;
- persistent attenuation;
- Catholic pastoral adequacy;
- model bias;
- or general embedding behaviour.

Those require source-grounded references, genuine held-out validation, sensitivity analysis, review, and benchmark freeze.

---

## 18. Documentation safeguards

Two documentation issues were identified during Step 1 reporting.

### Regex replacements

When generated Markdown contains backslashes such as `\Delta`, do not pass it directly as a regex replacement string.

Use a callable:

    updated = pattern.sub(
        lambda _: replacement_text,
        original,
        count=1,
    )

### GitHub mathematics

Use:

- `$...$` for inline mathematics;
- paired standalone `$$` lines for display mathematics.

Do not rely on backslash-plus-parenthesis or backslash-plus-square-bracket delimiters in GitHub documentation.

Avoid broad detectors that mistake explanatory prose about legacy notation for actual malformed equations. Prefer targeted conversion and inspect the Markdown diff.

---

## 19. Standard commands

Validate the fixture:

    .venv/bin/python scripts/ctsb_v3_4_prototype.py validate \
      --data-dir data/benchmarks/v3_4/prototype \
      --mode fixture

Run tests:

    .venv/bin/python tests/test_ctsb_v3_4_prototype.py

Run deterministic mock analysis:

    .venv/bin/python scripts/ctsb_v3_4_prototype.py run \
      --backend mock \
      --mode fixture

Run Azure fixture analysis:

    .venv/bin/python scripts/ctsb_v3_4_prototype.py run \
      --backend azure \
      --mode fixture

Build the standard lean AI context:

    ./tools/build_ai_context.sh

Build a context that also includes the full development log:

    ./tools/build_ai_context.sh --full

Include selected legacy v2 implementation files only when explicitly necessary:

    ./tools/build_ai_context.sh --with-legacy-v2

---

## 20. User workflow preferences

The user works primarily through macOS Terminal.

When proposing modifications:

- provide one complete Bash block;
- begin with `bash <<'BASH'` and `set -euo pipefail`;
- use timestamped backups;
- avoid manual editor instructions;
- use HTTPS GitHub remotes;
- use `gh` CLI;
- do not expose secrets;
- validate before committing;
- print useful final paths and Git status;
- keep the implementation lean unless complexity justifies expansion.

---

## 21. Handoff summary for the next AI

The project is no longer methodology-only.

A five-audit synthetic CTSB v3.4 prototype has been implemented, tested locally, run successfully against Azure `text-embedding-3-large`, documented, committed, and pushed.

The prototype is technically successful but non-evidential.

The next task is not another synthetic run, a dashboard, or immediate 100-concept expansion.

The next task is:

> Construct a source-grounded, independently reviewable five-audit pilot using the existing four-file data structure and integrated Python engine, then add validation and sensitivity checks before scaling.
