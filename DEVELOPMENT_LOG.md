# Development Log

<a id="step-1-2026-07-12"></a>
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

- [Audit definitions](data/benchmarks/v3_4/prototype/comparisons.csv)
- [Synthetic Catholic and comparison references](data/benchmarks/v3_4/prototype/references.csv)
- [Controlled contextual queries and registered baselines](data/benchmarks/v3_4/prototype/queries.csv)
- [Synthetic clear-register, integrative, and critical validation passages](data/benchmarks/v3_4/prototype/validation.csv)
- [Integrated prototype analysis script](scripts/ctsb_v3_4_prototype.py)
- [Automated prototype tests](tests/test_ctsb_v3_4_prototype.py)
- [Benchmark construction documentation](data/benchmarks/v3_4/README.md)

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

$$
CAS(q)=S_C(q)-S_R(q)
$$

For every registered query contrast:

$$
\Delta CAS=CAS(q_1)-CAS(q_0)
$$

and:

$$
\Delta CAS=\Delta S_C-\Delta S_R
$$

The maximum recorded decomposition error was:

$$
2.775557561563e-17
$$

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

<!-- BEGIN 2026-07-12 DOCUMENTATION-SAFEGUARDS -->
### Appendix: documentation corrections and safeguards

Two documentation-generation issues were identified and corrected during the recording of CTSB v3.4 Step 1. Neither issue affected the prototype data, Python calculations, Azure embeddings, or numerical results.

#### 1. Literal replacement text in Python regular expressions

The first documentation update raised:

    re.error: bad escape \D

The generated Markdown included LaTeX commands such as `\Delta`. When that Markdown was passed directly as the replacement-string argument to `re.sub()` or `Pattern.sub()`, Python attempted to interpret the backslashes as regex replacement-template syntax.

For generated Markdown or any other replacement text that may contain backslashes, future updates must use a callable replacement:

    updated_text = pattern.sub(
        lambda _: replacement_text,
        original_text,
        count=1,
    )

The callable return value is inserted literally. This protects LaTeX commands, paths, source code, and possible sequences resembling regex backreferences.

The same practice should be used for README replacements even when the present replacement text has no backslashes, because later revisions may introduce them.

#### 2. GitHub-compatible mathematical notation

GitHub Markdown should use dollar-sign math delimiters.

Inline mathematics should be written as:

    $CAS(q)=S_C(q)-S_R(q)$

Display mathematics should be written as:

    $$
    \Delta CAS=\Delta S_C-\Delta S_R
    $$

The earlier backslash-plus-square-bracket display notation was rendered as ordinary bracketed text on GitHub rather than as a mathematical block. The affected development-log equations were converted to double-dollar display blocks.

#### 3. Why no global legacy-delimiter rejection is used

A previous correction attempted to reject every occurrence of legacy math-delimiter character sequences. That check also detected explanatory prose describing the obsolete notation itself and stopped the update before writing the corrected file.

Future documentation maintenance should therefore:

- target actual standalone math-delimiter lines;
- use callable regex replacements;
- review the resulting Markdown diff;
- verify the relevant rendered GitHub page;
- and avoid broad rejection rules that cannot distinguish notation from explanatory prose.

#### 4. Required precautions for future development-log updates

Future automated documentation changes should:

1. create a timestamped backup;
2. use `pathlib` and `shutil.copy2` for safe file handling;
3. use callable replacements when regex is necessary;
4. prefer direct string replacement when a unique literal anchor is sufficient;
5. use `$...$` for inline GitHub math;
6. use paired standalone `$$` lines for display math;
7. run `git diff --check`;
8. inspect the Markdown headings and changed sections before committing;
9. preserve links to the original tracked CSV and Python files;
10. keep synthetic fixture outputs explicitly non-evidential;
11. keep `.env`, API keys, embedding caches, and private credentials outside Git;
12. avoid allowing documentation failures to modify benchmark data or numerical outputs.

#### 5. Scope of the documentation issues

The errors occurred only while generating or rendering the written development record. They did not change:

- `data/benchmarks/v3_4/prototype/comparisons.csv`;
- `data/benchmarks/v3_4/prototype/references.csv`;
- `data/benchmarks/v3_4/prototype/queries.csv`;
- `data/benchmarks/v3_4/prototype/validation.csv`;
- `scripts/ctsb_v3_4_prototype.py`;
- `tests/test_ctsb_v3_4_prototype.py`;
- the mock run;
- the Azure run;
- the 3,072-dimensional vectors;
- the query-to-reference cosine similarities;
- the CAS scores;
- or the shift-decomposition identity.

The original tracked Step 1 inputs remain available at:

- [Audit definitions](data/benchmarks/v3_4/prototype/comparisons.csv)
- [Synthetic reference anchors](data/benchmarks/v3_4/prototype/references.csv)
- [Controlled contextual queries](data/benchmarks/v3_4/prototype/queries.csv)
- [Synthetic validation passages](data/benchmarks/v3_4/prototype/validation.csv)
- [Integrated prototype script](scripts/ctsb_v3_4_prototype.py)
- [Automated prototype tests](tests/test_ctsb_v3_4_prototype.py)
<!-- END 2026-07-12 DOCUMENTATION-SAFEGUARDS -->

<a id="methodology-redesign-2026-07-10"></a>
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
  
  $$
  \Delta CAS=\Delta S_C-\Delta S_R
$$

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

<!-- BEGIN V3_5_ALPHA_GENERATED_100_20260713 -->
## CTSB v3.5-alpha generated 100-concept expansion — 13 July 2026

A generated exploratory 100-concept benchmark was added as CTSB v3.5-alpha.

The alpha contains 100 audits, 600 generated references, 1,624 queries, 808 generated development-validation passages, and eight critical-context audits. It retains the five v3.4 audits and uses explicitly named comparison registers and pre-assigned theological relationship types.

A deterministic mock run passed structural, mathematical, hashing, leave-one-reference-out, and paraphrase-analysis code paths. CAS reconstruction and shift decomposition were exact within floating-point precision.

The mock results are not semantic evidence. Perfect generated validation reflects shared construction fields and is not independent held-out validation.

All generated references remain marked as unreviewed, non-evidential, and pending exact-source, theological, and disciplinary review. Human review is formally deferred to future work rather than represented as complete.

Before evidential use, the project still requires exact source verification, reviewed reference wording, genuinely independent validation, ethical review of critical passages, benchmark freeze, and a final post-freeze model run.

Generated vectors, caches, and run outputs remain local and excluded from Git.
<!-- END V3_5_ALPHA_GENERATED_100_20260713 -->

<!-- BEGIN V3_5_ALPHA_COMPLETE_20260713 -->
## CTSB v3.5-alpha generated 100-concept experiment — 13 July 2026

### Milestone status

CTSB v3.5-alpha completed:

- generated 100-concept benchmark construction;
- structural validation;
- deterministic mock analysis;
- expanded sensitivity analysis;
- documentation safeguards;
- five new automated tests;
- successful Azure/OpenAI integration;
- component-level and robustness analysis;
- and preparation of the CTSB v3.5-beta handoff.

The alpha is technically complete but remains **generated, unreviewed, and non-evidential**.

The next planned phase is CTSB v3.5-beta.

---

### 1. User-led research-question clarification

During the alpha iteration, the research purpose was clarified substantially.

The central research contribution is not the predictable observation that adding Catholic or theological vocabulary increases proximity to Catholic references.

The user emphasised two deeper concerns.

#### 1.1 Theological adequacy under ambiguity

The project must examine concepts whose theological significance is implicit, morally contested, pastorally vulnerable, or semantically shared with other disciplines.

The important questions are:

- which register the model foregrounds under natural ambiguity;
- whether Catholic theological meaning remains accessible without an overt label;
- whether valid proximate meanings and theological meaning remain jointly accessible;
- and whether crisis wording reorganises the semantic field.

#### 1.2 Theological framing–content divergence

The user also identified a possible discrepancy between Catholic surface framing and substantive theological representation.

A system may use Catholic terminology or appear contextually Catholic while its underlying semantic organisation remains:

- autonomy-centred;
- biological;
- psychological;
- clinical;
- legal;
- affective;
- generic-religious;
- or otherwise theologically reduced or off-target.

This could create a downstream **illusion of theological adequacy**.

The project avoids attributing consciousness, a subconscious, belief, hostility, or intentional deception to an embedding model.

The adopted scientific terms include:

- default semantic tendency;
- latent representational prior;
- context-resistant register pull;
- residual comparison-register dominance;
- surface contextualisation without substantive recovery;
- and theological framing–content divergence.

The complete revised research questions are maintained in section 4 of `README.md`.

---

### 2. Decision to create CTSB v3.5-alpha

Exact source review and independent human review could not be completed during this development period.

The project therefore did not misrepresent generated statements as verified sources.

Instead, it created:

> **CTSB v3.5-alpha — a generated exploratory 100-concept benchmark**

The alpha was designed to test expanded implementation, Azure integration, component decomposition, and robustness analysis.

Every generated reference remained marked:

- `generated_unreviewed`;
- `human_review_pending`;
- candidate source only;
- not a quotation;
- not a verified paraphrase;
- not a verified summary;
- and non-evidential.

Generated validation passages were explicitly described as development validation rather than independent held-out validation.

---

### 3. Benchmark expansion

The alpha retained the CTSB v3.4 mathematical instrument and expanded from five audits to 100.

#### 3.1 Four theological loci

The generated benchmark contains 25 audits in each locus:

1. Freedom, Truth, and Moral Teleology;
2. Human Dignity and Theological Anthropology;
3. Love, Communion, and Sacramentality;
4. Sin, Grace, and Redemption.

#### 3.2 Relationship distribution

| Relationship type | Audits |
|---|---:|
| Valid but partial | 56 |
| Alternative lexical senses | 16 |
| Complementary levels | 14 |
| Generic religious versus Catholic-specific | 11 |
| Normatively conflicting | 3 |

This distribution is not statistically balanced. It reflects the generated development registry and must not be described as a representative sampling of all theological relationships.

#### 3.3 Retained v3.4 audits

The five original v3.4 audits were integrated into the 100-audit structure:

- `death_biological`;
- `grief_psychological`;
- `euthanasia_assisted_dying`;
- `grace_lexical`;
- `judgment_after_death_generic`.

#### 3.4 Generated data counts

| Table | Rows |
|---|---:|
| Comparisons | 100 |
| References | 600 |
| Queries | 1,624 |
| Validation passages | 808 |
| Clear-register validation passages | 600 |
| Critical-context audits | 8 |

Each audit received:

- three Catholic references;
- three comparison references;
- three natural paraphrases for major conditions;
- strict label-free/explicit-Catholic pairs;
- three generated Catholic validation passages;
- three generated comparison validation passages;
- two generated integrative passages;
- and a critical passage where applicable.

The broad v2 secular/common-language category was not restored.

---

### 4. Implementation-delivery iteration and recovery

The initial long terminal patch was interrupted while the 100-concept registry and alpha script were being delivered.

No partial shell block had executed before the interruption.

The continuation resumed from the interrupted registry line rather than regenerating the completed portion. The user merged the continuation into the saved command.

The completed script was then:

- written to `scripts/ctsb_v3_5_alpha.py`;
- marked executable;
- syntax checked with `py_compile`;
- used to generate all four alpha CSV tables;
- structurally validated;
- and run through the deterministic mock backend.

This delivery issue affected only transmission of the patch. It did not affect the generated benchmark or analysis results.

---

### 5. Alpha analysis implementation

The alpha script reused the v3.4 engine and added:

- deterministic 100-audit data generation;
- strict 100-audit and four-locus validation;
- preservation of source and review warnings;
- exact label-pair validation;
- concept-level condition summaries;
- bootstrap intervals over concepts;
- paired sign-flip diagnostics;
- leave-one-reference-out scoring;
- leave-one-reference-out sign stability;
- paraphrase-condition sensitivity;
- paraphrase leave-one-out summaries;
- paraphrase shift sensitivity;
- alpha-specific manifests;
- and non-evidential run reports.

The active script continued to export:

- raw vectors;
- embedding indexes;
- complete reference-level similarities;
- query scores;
- validation scores;
- nearest references;
- matched shifts;
- condition summaries;
- and validation metrics.

Raw vectors, caches, and generated runs remained local.

---

### 6. Initial Git-ignore problem and safeguard correction

After the first mock run, Git status showed:

- the new alpha benchmark;
- the new alpha script;
- and `outputs/` as untracked.

The generated outputs were not yet protected by the active `.gitignore`.

This was corrected before any commit.

The repository safeguards now exclude:

- `.env`;
- `.venv/`;
- Python bytecode;
- `outputs/`;
- `ai_context/`;
- `_patch_backups/`;
- and local operating-system artifacts.

A direct `git check-ignore` verification confirmed that alpha run manifests and generated outputs were ignored.

No vectors, caches, result directories, backups, context bundles, or secrets were committed.

---

### 7. Automated testing

Five existing CTSB v3.4 regression tests passed.

Five new CTSB v3.5-alpha tests passed:

1. registry balance and retention of the five v3.4 audits;
2. generated table counts and structural validation;
3. preservation of non-evidential source and review markers;
4. exact label-free/explicit-Catholic minimal pairs;
5. complete mock pipeline, manifest, CAS reconstruction, decomposition, similarity counts, and leave-one-reference-out outputs.

The alpha test suite completed in approximately seven seconds during the documented run.

The completed alpha benchmark, script, documentation, and tests were committed and pushed as:

- commit: `3d8c92d`;
- message: `Add CTSB v3.5-alpha generated 100-concept benchmark`.

---

### 8. Deterministic mock run

Local mock run ID:

`v3_5_alpha_mock_20260713-004555`

The mock backend used 256-dimensional lexical-hashing vectors.

#### 8.1 Integrity checks

- audits: 100;
- query scores: 1,624;
- matched shifts: 1,524;
- validation scores: 808;
- reference-level similarities: 14,592;
- maximum CAS reconstruction error: approximately $1.67\times10^{-16}$;
- maximum decomposition error: approximately $2.22\times10^{-16}$;
- all query scores finite;
- cosine range: -0.1618 to 0.9561;
- manifest hashes verified.

#### 8.2 Mock aggregate results

| Condition | Mean $S_C$ | Mean $S_R$ | Mean CAS |
|---|---:|---:|---:|
| Bare | 0.2287 | 0.2430 | -0.0143 |
| Natural general | 0.1699 | 0.7066 | -0.5367 |
| Natural ambiguous | 0.1236 | 0.1222 | +0.0015 |
| Label-free theological | 0.8094 | 0.1872 | +0.6222 |
| Explicit Catholic | 0.7840 | 0.1849 | +0.5991 |
| Integrative | 0.6142 | 0.5267 | +0.0875 |
| Critical | 0.1125 | 0.1281 | -0.0156 |

The mock output largely reflected lexical construction and was not interpreted as semantic evidence.

#### 8.3 Mock sensitivity

- 1,491 of 1,624 queries were sign-stable under every reference omission;
- mean leave-one-reference-out sign stability: 0.9755;
- largest absolute leave-one-reference-out CAS change: 0.1137;
- 97 of 508 audit-condition groups had mixed CAS signs across paraphrases;
- nine audit-contrast groups had mixed $\Delta CAS$ signs;
- maximum condition CAS standard deviation: 0.1990.

The mock confirmed that the sensitivity code paths worked.

---

### 9. Azure run

Azure run ID:

`v3_5_alpha_azure_20260713-010232`

Run Git commit:

`3d8c92dfe0807363d8e424202ece7a42bc60b28c`

#### 9.1 Azure integration details

- provider: Azure OpenAI;
- requested model: `text-embedding-3-large`;
- deployment: `text-embedding-3-large-prova1`;
- Azure-reported model: `text-embedding-3-large`;
- dimensions: 3,072;
- unique texts: 3,032;
- new embeddings: 3,032;
- cached embeddings: 0;
- batches: 48;
- batch size: 64.

No API key, endpoint, token, or secret value was printed.

#### 9.2 Azure output integrity

- audits: 100;
- query scores: 1,624;
- matched shifts: 1,524;
- validation scores: 808;
- reference-level similarities: 14,592;
- maximum CAS reconstruction error: approximately $2.22\times10^{-16}$;
- maximum decomposition error: approximately $5.55\times10^{-17}$;
- all query scores finite;
- cosine range: 0.1522 to 0.9747;
- manifest hashes verified;
- core Azure integration check passed.

---

### 10. Azure condition-level results

| Condition | Concepts | Mean $S_C$ | Mean $S_R$ | Mean CAS | Median CAS | Positive CAS |
|---|---:|---:|---:|---:|---:|---:|
| Bare | 100 | 0.4679 | 0.5021 | -0.0342 | -0.0372 | 25% |
| Natural general | 100 | 0.5166 | 0.7600 | -0.2434 | -0.2474 | 0% |
| Natural ambiguous | 100 | 0.4900 | 0.4963 | -0.0063 | -0.0086 | 42% |
| Label-free theological | 100 | 0.8067 | 0.5224 | +0.2843 | +0.2774 | 100% |
| Explicit Catholic | 100 | 0.8919 | 0.4694 | +0.4226 | +0.4220 | 100% |
| Integrative | 100 | 0.7094 | 0.6757 | +0.0338 | +0.0322 | 70% |
| Critical | 8 | 0.3966 | 0.4198 | -0.0232 | -0.0305 | 37.5% |

The critical-context bootstrap interval crossed zero.

These values describe the generated alpha benchmark only.

---

### 11. Azure matched shifts

| Contrast | Concepts | Mean $\Delta S_C$ | Mean $\Delta S_R$ | Mean $\Delta CAS$ | Positive $\Delta CAS$ |
|---|---:|---:|---:|---:|---:|
| Bare to general | 100 | +0.0487 | +0.2579 | -0.2092 | 0% |
| General to ambiguous | 100 | -0.0267 | -0.2637 | +0.2370 | 100% |
| General to label-free theological | 100 | +0.2901 | -0.2376 | +0.5277 | 100% |
| Label-free to explicit Catholic | 100 | +0.0852 | -0.0531 | +0.1383 | 100% |
| General to integrative | 100 | +0.1928 | -0.0844 | +0.2772 | 100% |
| General to critical | 8 | -0.0752 | -0.3302 | +0.2550 | 100% |

The sign-flip diagnostics were small for all generated contrasts. They are not treated as independent scientific evidence because the shift directions were strongly influenced by shared construction templates.

---

### 12. Central decomposition insight

The alpha gave a clear demonstration of why CAS must be decomposed.

For general to ambiguous:

- Catholic similarity declined by 0.0267;
- comparison similarity declined by 0.2637;
- CAS increased by 0.2370.

For general to critical:

- Catholic similarity declined by 0.0752;
- comparison similarity declined by 0.3302;
- CAS increased by 0.2550.

In both cases, a positive relative shift could be misreported as theological recovery.

The component scores show that Catholic-reference proximity actually declined.

This is a successful methodological demonstration of:

> apparent recovery without theological association gain.

---

### 13. Critical-context results

| Audit | Mean $S_C$ | Mean $S_R$ | Mean CAS |
|---|---:|---:|---:|
| Death | 0.3295 | 0.3693 | -0.0397 |
| Dying | 0.4954 | 0.4441 | +0.0513 |
| Euthanasia | 0.4192 | 0.5243 | -0.1051 |
| Grief | 0.3884 | 0.4138 | -0.0253 |
| Illness | 0.3429 | 0.3124 | +0.0306 |
| Palliative care | 0.4775 | 0.4734 | +0.0040 |
| Suffering | 0.3554 | 0.3911 | -0.0357 |
| Suicide | 0.3644 | 0.4303 | -0.0658 |

The most comparison-oriented generated critical cases were euthanasia and suicide.

These values do not establish pastoral inadequacy.

For suicide, mental-health salience may be clinically necessary and safety-relevant.

Several critical paraphrases crossed zero, showing that wording remained consequential.

---

### 14. Azure robustness results

#### 14.1 Leave-one-reference-out

- 1,461 of 1,624 queries retained the same CAS sign under every individual reference omission;
- 163 queries changed sign under at least one omission;
- mean sign stability: 0.9710;
- minimum sign stability: 0.3333;
- largest absolute CAS change: 0.0936.

Approximately 90% of queries were fully sign-stable, but borderline cases remained reference-sensitive.

#### 14.2 Paraphrase sensitivity

- 137 of 508 audit-condition groups had mixed CAS signs across paraphrases;
- no audit-contrast group had mixed $\Delta CAS$ direction;
- median condition CAS standard deviation: 0.0324;
- maximum condition CAS standard deviation: 0.1339;
- median shift $\Delta CAS$ standard deviation: 0.0313;
- maximum shift $\Delta CAS$ standard deviation: 0.1323.

Approximately 27% of audit-condition groups crossed the CAS zero boundary across paraphrases.

This shows that absolute near-zero classifications were less stable than the generated shift directions.

---

### 15. Generated validation result and construction leakage

Generated clear-register validation produced:

- balanced accuracy: 1.0;
- Catholic recall: 1.0;
- comparison recall: 1.0;
- macro F1: 1.0.

This is not evidence of independent instrument validity.

References and validation passages were generated from the same concept fields and used related templates.

The alpha therefore contains:

- phrase reuse;
- concept-field reuse;
- predictable register wording;
- repeated Catholic identifiers;
- and condition-specific construction effects.

The perfect validation result demonstrates that the pipeline can separate deliberately constructed fields. It does not establish performance on independently authored natural texts.

---

### 16. Interpretation of the explicit Catholic effect

Moving from label-free theological content to explicit Catholic framing produced:

- mean $\Delta S_C=+0.0852$;
- mean $\Delta S_R=-0.0531$;
- mean $\Delta CAS=+0.1383$;
- positive $\Delta CAS$ in all 100 audits.

This is a measurable generated-benchmark-relative label effect.

It is not yet evidence of general model label dependence because the Catholic reference anchors repeatedly contain Catholic-identifying language.

Beta must reduce this confound by separating provenance metadata from anchor wording and balancing label frequency.

---

### 17. Interpretation of integrative contexts

Integrative queries had:

- mean $S_C=0.7094$;
- mean $S_R=0.6757$;
- mean CAS $=+0.0338$.

The relatively high component similarities suggest that the analysis can detect proximity to both fields.

However, raw cosine values do not yet provide a calibrated universal threshold for joint accessibility.

Beta should interpret component scores relative to independently validated Catholic, comparison, and integrative distributions.

---

### 18. What the alpha established

The alpha supports the following implementation claims:

- the 100-audit data model works;
- the v3.4 mathematics scale to 100 audits;
- Azure integration works for 3,032 unique texts;
- the endpoint returns the expected model family and dimensions;
- full reference-level scoring works;
- component shifts reconstruct correctly;
- leave-one-reference-out analysis works;
- paraphrase analysis works;
- statistical summaries work;
- local run manifests and hashes work;
- and the instrument can distinguish theological gain from comparison suppression.

---

### 19. What the alpha did not establish

The alpha does not support final claims about:

- Catholic theological legibility;
- persistent theological attenuation;
- context-resistant anti-theological bias;
- Catholic pastoral adequacy or inadequacy;
- doctrinal specificity;
- theological framing–content divergence in natural language;
- retrieval quality;
- generated-answer correctness;
- user deception;
- or user trust.

The generated design currently demonstrates the instrument more strongly than it measures natural model behaviour.

---

### 20. Revised research contribution

The project’s intended contribution is now stated more precisely:

> The project asks whether an embedding model can appear appropriately Catholic through vocabulary and framing while its substantive semantic organisation remains reduced, generic, context-resistant, or dominated by another register.

The intended final product is a theological calibration map showing:

- where theological meaning is stable;
- where it is accessible without labels;
- where it is jointly accessible with valid proximate meanings;
- where it is recovered through substantive content;
- where it depends on explicit labels;
- where apparent recovery is caused by displacement;
- where Catholic specificity is replaced by generic religion;
- and where theological meaning remains fragile.

---

### 21. CTSB v3.5-beta decision

The next phase is CTSB v3.5-beta.

Beta should not begin by regenerating all 100 audits or rerunning Azure.

The immediate beta task is a focused construction pilot designed to reduce alpha leakage.

Required beta priorities are:

1. natural queries not copied from reference fields;
2. separate authoring streams for references, queries, and validation;
3. reduced repeated Catholic labels in anchor bodies;
4. provenance stored in metadata rather than semantic labels;
5. lexical and n-gram overlap diagnostics;
6. label-frequency checks;
7. independently authored development validation;
8. validation-based calibration of $S_C$ and $S_R$;
9. predeclared framing–content divergence indicators;
10. ethical and disciplinary safeguards for critical contexts;
11. benchmark freeze before another Azure run;
12. continued non-evidential labelling if source and human review remain deferred.

A focused beta pilot of approximately 12 strategically chosen concepts is preferred before deciding whether to revise all 100.

---

### 22. Dashboard and evidence policy

Dashboard work remains deferred.

Numerical high-dimensional analysis remains primary.

No local alpha vectors, caches, run directories, diagnostic reports, backups, secrets, or context bundles are to be committed.

The alpha Azure outputs remain locally available under:

`outputs/v3_5_alpha/runs/v3_5_alpha_azure_20260713-010232/`

The standard AI context bundle should contain the active handoff, current research questions, beta plan, active code, and tests while omitting local generated runs and unnecessary historical data.
<!-- END V3_5_ALPHA_COMPLETE_20260713 -->
