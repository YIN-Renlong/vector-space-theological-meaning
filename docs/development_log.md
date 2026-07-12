# Development Log

## 10 July 2026 — CTSB v3.4 methodology redesign

### Status

CTSB-100 v2 has been archived. The active project has entered a methodology-design phase. No v3.4 benchmark results have yet been generated.

### Questions raised during methodological review

The redesign was motivated by several foundational questions:

1. Does negative CAS demonstrate “common language,” and how is that category defined?
2. What model is being audited, and what text is known to have trained it?
3. What can be concluded from the plots, and what cannot?
4. How can a numerical embedding result be identified as Catholic?
5. Does a positive contrast shift represent increased Catholic proximity or only reduced comparison proximity?
6. Are psychological, biological, clinical, legal, social, and theological meanings mutually exclusive?
7. Why audit an embedding model rather than a generative chatbot?
8. How can the method remain useful to theologians without treating cosine similarity as theological authority?

Attribution for externally raised review questions will be added only with the reviewer's permission.

### Main v3.4 decisions

- Rename the metric **Catholic Association Contrast**.
- Treat CAS as a relative association statistic, not a probability or truth score.
- Embed both queries and known natural-language references.
- Interpret vectors through their measured relationships to source-grounded references.
- Preserve the original natural-language text attached to every reference vector.
- Distinguish complementary, partial, conflicting, lexical, and generic-religious relationships.
- Validate the instrument on held-out texts.
- Retain separate Catholic and comparison similarities alongside their difference.
- Decompose every context shift as:
  
  \[
  \Delta CAS=\Delta S_C-\Delta S_R
  \]

- Introduce natural ambiguity and critical-context conditions.
- Keep visualisations secondary to high-dimensional numerical analysis.
- Reserve generative GPT and retrieval-system audits for future work.

### Archived v2 findings

The v2 results remain historical preliminary evidence. They are not automatically carried forward as v3.4 conclusions.

The following patterns will be independently re-tested:

- explicit Catholic wording produced a strong relative shift;
- explicitly doctrinal concepts appeared comparatively stable;
- moral-teleological concepts showed autonomy-, choice-, permission-, and well-being-centred foregrounding;
- anthropological concepts showed biological, functional, economic, and legal foregrounding;
- life/death concepts showed clinical, psychological, biological, legal, and crisis-related foregrounding;
- grief, suicide, euthanasia, chastity, autonomy, shame, and license appeared comparatively resistant.

### Next implementation stage

The next stage will design the v3.4 benchmark schema and source-review workflow.

The v3.4 Python audit must be written separately. The archived v2 script does not implement the v3.4 protocol.

## 12 July 2026 — CTSB v3.4 Step 1: synthetic prototype and Azure integration

### 1. Milestone status

CTSB v3.4 Step 1 was completed on 12 July 2026.

The completed milestone is a **lean, non-evidential development prototype**. It demonstrates that the redesigned v3.4 data model, Azure embedding connection, Catholic Association Contrast calculations, matched contextual contrasts, held-out scoring workflow, shift decomposition, and machine-readable exports operate together correctly.

This milestone is not the final benchmark and does not establish substantive findings about Catholic theology or the audited embedding model. All reference and validation texts used in this step are synthetic development fixtures.

The implementation was committed in Git commit `000b20d` with the message:

> Add CTSB v3.4 synthetic analysis prototype

### 2. Methodological clarifications reached during interactive design

The prototype emerged through an iterative clarification process rather than by copying v2.

#### 2.1 v2 remains historical only

The archived v2 benchmark tested 100 concepts and 1,000 query rows using five Catholic descriptors and five broad “secular/common-language” descriptors per concept.

The v3.4 redesign does not reuse that broad comparison category. Psychological, biological, clinical, legal, lexical, social, economic, ordinary-language, and generic-religious meanings are not assumed to form one coherent opposing class.

v2 now serves only to:

- motivate concepts and hypotheses for re-testing;
- provide historical API and cosine-calculation reference;
- and document the development history of the project.

No v2 result is treated as a v3.4 finding.

#### 2.2 The implementation was deliberately simplified

An initial production-style proposal divided the pipeline into many registries and Python modules. Because this stage is a prototype, that design was simplified to:

- four linked CSV files;
- one integrated Python script;
- one automated test file;
- and one standard output directory per run.

This preserves the methodological distinctions without prematurely over-engineering the software.

#### 2.3 Queries and references have different evidential roles

Experimental queries do not require documentary citations. They are controlled model inputs authored for the experiment.

Reference texts have a different role: they operationally define the Catholic and comparison semantic fields used in CAS. The present fixture references are explicitly marked synthetic, so they are sufficient only for code testing.

The future empirical benchmark will replace them with short references grounded in identifiable Catholic and disciplinary sources. The lean CSV design already retains:

- `source_title`;
- `source_location`;
- `text_status`;
- `review_status`;
- and `review_notes`.

#### 2.4 Life and Death is integrated into the unified benchmark

The v2 Life and Death supplement was implemented separately. In v3.4, Life and Death is a pre-specified analytical module inside the same benchmark and Python pipeline.

A concept can therefore retain its primary theological locus and also carry `life_death_module=true`. It must not be duplicated and counted as an independent concept twice.

#### 2.5 CTSB v3.4 is an original domain-specific synthesis

The method combines established or strongly precedented techniques:

- differential cosine association;
- reference-based embedding comparison;
- controlled contextual contrasts;
- minimal-pair label perturbation;
- held-out validation;
- ranking;
- and paired change analysis.

The theological operationalisation is project-specific:

- named comparison registers;
- five pre-assigned theological relationship types;
- label-free theological versus explicit Catholic wording;
- component-level shift decomposition;
- integrative-register analysis;
- and critical-context theological accessibility.

This synthesis constitutes the project's methodological contribution. It is not yet an independently peer-reviewed or universally validated instrument, and no historical-priority claim is made without a systematic literature review.

### 3. Prototype audit units

Five illustrative audit units were selected so that the fixture covers all five theological relationship types.

| Audit ID | Concept | Comparison register | Relationship type | Life and Death module |
|---|---|---|---|---|
| `death_biological` | death | biological description | complementary levels | yes |
| `grief_psychological` | grief | psychological bereavement | valid but partial | yes |
| `euthanasia_assisted_dying` | euthanasia | permissive assisted-dying register | normatively conflicting | yes |
| `grace_lexical` | grace | elegance and social charm | alternative lexical senses | no |
| `judgment_after_death_generic` | judgment after death | generic religious afterlife judgment | generic religious versus Catholic-specific | yes |

These five audit units are methodological examples, not the frozen concept list for the final benchmark.

### 4. Primary prototype source files

The original tracked fixture inputs are:

- [Audit definitions](../data/benchmarks/v3_4/prototype/comparisons.csv)
- [Synthetic Catholic and comparison references](../data/benchmarks/v3_4/prototype/references.csv)
- [Controlled contextual queries and registered baselines](../data/benchmarks/v3_4/prototype/queries.csv)
- [Synthetic clear-register, integrative, and critical validation passages](../data/benchmarks/v3_4/prototype/validation.csv)
- [Integrated prototype analysis script](../scripts/ctsb_v3_4_prototype.py)
- [Automated prototype tests](../tests/test_ctsb_v3_4_prototype.py)
- [Benchmark construction documentation](../data/benchmarks/v3_4/README.md)

The four fixture files contain:

- 5 audit units;
- 30 references;
- 32 queries;
- 28 validation passages;
- and 20 clear-register validation passages.

Each audit contains three synthetic Catholic references and three synthetic comparison references.

### 5. Query conditions tested

The fixture tested the applicable subset of the v3.4 query conditions:

- bare concept;
- natural general context;
- natural ambiguity;
- critical context where declared applicable;
- label-free theological content;
- explicit Catholic contextualisation;
- and integrative theological-proximate content.

The principal registered contrasts were:

- bare to natural general;
- general to ambiguous;
- general to critical;
- general to label-free theological;
- label-free theological to explicit Catholic;
- and general to integrative.

The label-free versus explicit-Catholic comparison is intended to distinguish movement caused by theological content from movement caused by an overt Catholic label.

### 6. Integrated Python implementation

The prototype script supports three commands:

    .venv/bin/python scripts/ctsb_v3_4_prototype.py write-fixture
    .venv/bin/python scripts/ctsb_v3_4_prototype.py validate
    .venv/bin/python scripts/ctsb_v3_4_prototype.py run --backend mock

The same `run` command also supports the Azure backend:

    .venv/bin/python scripts/ctsb_v3_4_prototype.py run --backend azure

The script performs:

1. CSV loading and structural validation;
2. ID and foreign-key checks;
3. controlled-vocabulary checks;
4. source-provenance enforcement in future `benchmark` mode;
5. deterministic mock embeddings for offline testing;
6. Azure embedding requests and local caching;
7. full query-to-reference cosine calculation;
8. within-audit and within-group reference ranking;
9. calculation of Catholic similarity `S_C`;
10. calculation of comparison similarity `S_R`;
11. calculation of `CAS = S_C - S_R`;
12. explicit matched-query shift calculation;
13. exact verification of `ΔCAS = ΔS_C - ΔS_R`;
14. clear-register validation metrics;
15. separate scoring of integrative and critical passages;
16. raw vector export;
17. file hashing;
18. and run-manifest generation.

The Azure cache key includes provider configuration, deployment, API version, dimensions, and exact input text. The active cache and `.env` remain excluded from Git.

### 7. Automated tests

Five automated tests passed:

1. fixture schema and linked-ID validation;
2. rejection of synthetic sources in final `benchmark` mode;
3. deterministic mock-embedding repeatability;
4. cosine identity for an identical vector;
5. complete mock-pipeline execution and output verification.

The complete test suite ran in approximately 0.17 seconds and returned `OK`.

Temporary fixture directories shown during testing were created by Python's test framework under macOS `/var/folders/`. They were isolated test data and not additional project benchmarks.

### 8. Mock-backend pipeline run

The first complete run used deterministic local lexical-hashing vectors:

    /Users/Renlong/Projects/GitHub/YIN-Renlong/vector-space-theological-meaning/outputs/v3_4/prototype_runs/fixture_mock_20260712-222901

Its purpose was to verify the pipeline without contacting Azure.

The perfect synthetic classification obtained in this run was not interpreted as evidence. The mock vectors and synthetic passages were designed only to test code paths and mathematical reconstruction.

### 9. Azure configuration correction

The first Azure preflight check stopped safely before sending any request because `.env` initially contained only:

- the Azure API key;
- and the Azure endpoint.

The preflight correctly identified the missing deployment and API-version variables.

The local `.env` was backed up and then completed with:

- deployment: `text-embedding-3-large-prova1`;
- API version: `2024-02-01`.

The API key was never printed or committed.

No new analysis code was needed. The existing integrated prototype already supported `--backend azure`.

### 10. Azure integration run

The successful Azure fixture run is stored locally at:

    /Users/Renlong/Projects/GitHub/YIN-Renlong/vector-space-theological-meaning/outputs/v3_4/prototype_runs/fixture_azure_20260712-223931

The primary local result files are:

- `/Users/Renlong/Projects/GitHub/YIN-Renlong/vector-space-theological-meaning/outputs/v3_4/prototype_runs/fixture_azure_20260712-223931/run_manifest.json`;
- `/Users/Renlong/Projects/GitHub/YIN-Renlong/vector-space-theological-meaning/outputs/v3_4/prototype_runs/fixture_azure_20260712-223931/query_scores.csv`;
- `/Users/Renlong/Projects/GitHub/YIN-Renlong/vector-space-theological-meaning/outputs/v3_4/prototype_runs/fixture_azure_20260712-223931/shifts.csv`;
- `/Users/Renlong/Projects/GitHub/YIN-Renlong/vector-space-theological-meaning/outputs/v3_4/prototype_runs/fixture_azure_20260712-223931/similarities.csv`;
- `/Users/Renlong/Projects/GitHub/YIN-Renlong/vector-space-theological-meaning/outputs/v3_4/prototype_runs/fixture_azure_20260712-223931/validation_scores.csv`;
- `/Users/Renlong/Projects/GitHub/YIN-Renlong/vector-space-theological-meaning/outputs/v3_4/prototype_runs/fixture_azure_20260712-223931/validation_metrics.csv`;
- `/Users/Renlong/Projects/GitHub/YIN-Renlong/vector-space-theological-meaning/outputs/v3_4/prototype_runs/fixture_azure_20260712-223931/azure_result_report.txt`;
- `embedding_index.csv`;
- and `embeddings.npz`.

Generated prototype-run outputs remain ignored by Git. They are local execution artifacts rather than frozen public benchmark results.

Azure run metadata:

| Field | Recorded value |
|---|---|
| Provider | `azure_openai` |
| Requested model | `text-embedding-3-large` |
| Azure deployment | `text-embedding-3-large-prova1` |
| Azure-reported model | `text-embedding-3-large` |
| API version | `2024-02-01` |
| Embedding dimensions | 3072 |
| Unique embedded texts | 90 |
| New embeddings | 90 |
| Cached embeddings | 0 |
| Azure batches | 2 |
| Query-score rows | 32 |
| Full similarity rows | 360 |
| Registered shift rows | 27 |
| Validation-score rows | 28 |

Azure returned 3,072-dimensional vectors and identified the response model as `text-embedding-3-large`.

### 11. Mathematical verification

The scoring identity was preserved:

\[
CAS(q)=S_C(q)-S_R(q)
\]

For every registered query contrast:

\[
\Delta CAS=CAS(q_1)-CAS(q_0)
\]

and:

\[
\Delta CAS=\Delta S_C-\Delta S_R
\]

The maximum recorded decomposition error was:

\[
2.775557561563e-17
\]

This is ordinary floating-point precision and confirms that the component decomposition was implemented correctly.

### 12. Synthetic clear-register validation

The clear-register fixture contained four passages per audit:

- two synthetic Catholic examples;
- and two synthetic comparison-register examples.

The Azure fixture produced:

| Measure | Result |
|---|---:|
| Clear-register passages | 20 |
| Balanced accuracy | 1.0000 |
| Catholic recall | 1.0000 |
| Comparison recall | 1.0000 |
| Macro F1 | 1.0000 |

This perfect score is a pipeline sanity check only. It is not genuine held-out construct validation because:

- the references and validation passages were authored during the same fixture-construction process;
- the registers were intentionally clear;
- lexical and conceptual overlap remains;
- each audit has only four clear validation passages;
- and all texts are synthetic.

The correct conclusion is that Azure and the prototype distinguished the deliberately clear fixture registers. The result does not predict final benchmark performance.

### 13. Initial fixture-relative observations

These observations are recorded to demonstrate the analytical value of the v3.4 outputs. They are not final empirical claims.

#### 13.1 General wording to label-free theological content

| Audit | ΔS_C | ΔS_R | ΔCAS |
|---|---:|---:|---:|
| Death × biological description | +0.4107 | -0.2859 | +0.6966 |
| Grief × psychological bereavement | +0.3231 | -0.1082 | +0.4313 |
| Euthanasia × permissive assisted dying | +0.2931 | -0.1430 | +0.4361 |
| Grace × elegance/social charm | +0.4467 | -0.4439 | +0.8906 |
| Judgment after death × generic religious judgment | +0.1969 | -0.1553 | +0.3522 |

Across all five synthetic audits:

- `S_C` increased;
- `S_R` decreased;
- and CAS increased.

Within this fixture, the movement was therefore produced by both theological association gain and register differentiation.

#### 13.2 Label-free theological content to explicit Catholic wording

| Audit | ΔS_C | ΔS_R | ΔCAS |
|---|---:|---:|---:|
| Death × biological description | -0.0810 | -0.0229 | -0.0581 |
| Grief × psychological bereavement | -0.0351 | -0.0198 | -0.0153 |
| Euthanasia × permissive assisted dying | -0.0330 | -0.0483 | +0.0153 |
| Grace × elegance/social charm | -0.0213 | +0.0997 | -0.1210 |
| Judgment after death × generic religious judgment | -0.0253 | -0.0521 | +0.0268 |

Adding the explicit Catholic label did not increase `S_C` in any of the five fixture audits.

Three CAS shifts were negative. Two were slightly positive, but those positive relative shifts occurred because `S_R` decreased more than `S_C`.

This is an important demonstration of the difference between:

- actual Catholic-reference proximity gain;
- and a positive relative contrast caused by comparison-register suppression.

It also shows why a positive CAS shift must not automatically be called Catholic activation.

These five synthetic examples are too few and too constructed to support a general claim that content matters more than labels. That proposition must be tested using reviewed minimal pairs and natural paraphrases.

#### 13.3 General wording to critical context

| Audit | ΔS_C | ΔS_R | ΔCAS |
|---|---:|---:|---:|
| Death × biological description | +0.1005 | -0.3674 | +0.4679 |
| Grief × psychological bereavement | -0.1387 | -0.1122 | -0.0264 |
| Euthanasia × permissive assisted dying | -0.0103 | -0.0894 | +0.0791 |

The three critical-context examples behaved differently:

- death increased `S_C`, while biological similarity decreased strongly;
- grief decreased both components and became slightly more comparison-associated;
- euthanasia had a positive CAS shift even though `S_C` declined, because `S_R` declined more.

The euthanasia case is the clearest fixture demonstration of relative movement without theological gain.

#### 13.4 General wording to integrative context

| Audit | ΔS_C | ΔS_R | ΔCAS |
|---|---:|---:|---:|
| Death × biological description | +0.3567 | -0.1692 | +0.5259 |
| Grief × psychological bereavement | +0.2612 | +0.0166 | +0.2447 |
| Euthanasia × permissive assisted dying | +0.2662 | -0.0913 | +0.3574 |
| Judgment after death × generic religious judgment | +0.0094 | -0.1501 | +0.1595 |

The integrative queries did not all behave alike:

- grief increased both `S_C` and `S_R`, giving the clearest fixture example of joint accessibility with theological enrichment;
- death and euthanasia increased `S_C` while decreasing `S_R`, which looks more like differentiation than joint enrichment;
- judgment after death changed `S_C` only slightly while reducing generic-religious similarity.

An input labelled integrative therefore cannot be assumed to produce joint accessibility. The component pair `(S_C, S_R)` must be examined.

#### 13.5 Mixed local and global association

The following fixture queries had disagreement between the mean-field CAS direction and the group of the single nearest reference:

| Query | Condition | CAS | Mean-field direction | Top reference group |
|---|---|---:|---|---|
| `euthanasia_ambiguous_1` | `natural_ambiguous` | +0.0009 | Catholic | Comparison |
| `grace_bare_1` | `bare` | +0.0151 | Catholic | Comparison |
| `judgment_bare_1` | `bare` | -0.0112 | Comparison | Catholic |
| `judgment_ambiguous_1` | `natural_ambiguous` | -0.0100 | Comparison | Catholic |

This confirms the utility of exporting both:

- mean reference-field contrasts;
- and nearest-reference rankings.

A single nearest reference and the average reference field can describe different aspects of local semantic behaviour.

### 14. Provenance and integrity record

The recorded Azure run manifest linked the run to the exact four fixture inputs through SHA-256 hashes.

| Recorded input | SHA-256 |
|---|---|
| `comparisons.csv` | `d499f153953a5f0bf6aec83f5458fdd3f8b6418c0246ff220847b57e6c31a8cf` |
| `queries.csv` | `68217a1fce49030c3f9321df5261f3564fc49e4916a227d269785ccd6c252699` |
| `references.csv` | `87870da25d49aee8000689c6ebcba9130ba15d6807e98d0573ad6a3e6d248eb5` |
| `validation.csv` | `cc0278d79e9a44bb470377d6fdb034a478ac84d9cae9de95f3feff80eb2d43c8` |
| `run_manifest.json` | `7432bf22c38af6ded24faf9ba22c233a77b27ca48d7401e7a0e413ba6167326f` |
| `azure_result_report.txt` | `800b2931957fd9487ec487f84a70b29e4f896eb1b57a2966b31e642ce92ae33b` |

These hashes identify the exact synthetic input version used for the Azure run. If any fixture file changes, the recorded run should no longer be treated as a result of the revised fixture.

### 15. Interpretation restrictions

No numerical result in this entry should be presented as:

- a final CTSB v3.4 result;
- evidence that Catholic theology is true or false;
- proof that the embedding model believes anything;
- proof of stable theological accessibility;
- validation of the final instrument;
- or evidence about ChatGPT's generated pastoral behaviour.

The prototype demonstrates:

- correct data flow;
- successful Azure integration;
- reproducible numerical scoring;
- exact shift decomposition;
- and the analytical usefulness of separating `S_C`, `S_R`, CAS, and nearest-reference rankings.

### 16. Step 1 conclusion

CTSB v3.4 Step 1 succeeded.

The project now has a working lean prototype that is methodologically distinct from v2 and capable of running both deterministic local tests and real Azure embeddings.

The most important technical result is that the new analysis can distinguish:

- theological association gain;
- comparison-register suppression;
- mixed component movement;
- label-related movement;
- critical-context change;
- integrative joint accessibility;
- and disagreement between local and global association.

### 17. Next substantive stage

Step 2 should remain a five-audit pilot before scaling to a full benchmark.

The next work is to:

1. replace synthetic Catholic references with short, verified, source-grounded references;
2. ground comparison references in appropriate psychological, biological, clinical, lexical, moral, or religious-studies sources;
3. construct genuinely separate held-out validation passages;
4. tighten label-free and explicit-Catholic minimal pairs;
5. add natural paraphrases for important conditions;
6. add leave-one-reference-out and paraphrase-sensitivity analysis;
7. pre-specify validation acceptance criteria;
8. run the five-audit source-grounded Azure pilot;
9. review the results before deciding the size of the final benchmark;
10. and only later construct the dashboard.
