# CTSB v3.5-alpha Dashboard Design

## 1. Dashboard identity

**Project:** Vector Space and Theological Meaning  
**Dashboard:** CTSB v3.5-alpha Generated Exploratory Results  
**Azure run:** `v3_5_alpha_azure_20260713-010232`  
**Public status:** Generated, unreviewed, exploratory, and non-evidential

This document is the controlling visual-design specification for the CTSB v3.5-alpha dashboard.

The dashboard should be suitable for presentation to a university professor while remaining:

- mathematically accurate;
- statistically responsible;
- methodologically clear;
- informed by NLP and embedding-evaluation practice;
- visually elegant;
- concise enough to understand in one sitting;
- accessible;
- and explicit about the limitations of the generated benchmark.

The visual design must serve the research questions. It must not simply display every available file or statistic.

---

## 2. Central research narrative

The dashboard should answer this central question:

> **Does Catholic theological meaning remain accessible under ambiguity and semantic competition, and can apparent theological recovery be distinguished from genuine Catholic-reference association gain?**

The main narrative is:

1. What semantic register is foregrounded under natural or ambiguous language?
2. Can Catholic theological and valid adjacent meanings remain jointly accessible?
3. Is theological substance legible without an overt Catholic label?
4. Does explicit Catholic framing produce substantive Catholic-reference recovery?
5. Can CAS become more positive even while Catholic-reference similarity declines?
6. What happens under pastorally or clinically critical language?
7. How sensitive are the observations to paraphrases and exact reference selection?

The predictable result that adding Catholic vocabulary increases Catholic association must remain a secondary diagnostic, not the dashboard's main conclusion.

---

## 3. Evidential warning

Display this warning prominently near the top and repeat a shorter version near the conclusion:

> **Generated exploratory alpha — non-evidential.** The references, queries, and validation passages were generated for instrument development and have not received exact-source, theological, disciplinary, or independent validation review. Results are relative to predefined generated reference fields and must not be interpreted as validated findings about Catholic theology, model bias, pastoral adequacy, or ChatGPT responses.

The dashboard must not imply:

- that CAS is a Catholic truth score;
- that negative CAS means hostility, error, or secularism;
- that positive CAS proves theological adequacy;
- that the embedding model has beliefs, intentions, consciousness, or a subconscious;
- that the model deliberately deceives users;
- that the model is pastorally adequate or inadequate;
- or that the results generalise to all embedding models or AI systems.

---

## 4. Public result-data strategy

The selected alpha result files are committed under:

    outputs/v3_5_alpha/runs/v3_5_alpha_azure_20260713-010232/

The dashboard should fetch these committed files directly through repository-relative paths.

When the dashboard is located at:

    dashboards/v3_5_alpha/index.html

the result files can be reached through paths such as:

    ../../outputs/v3_5_alpha/runs/v3_5_alpha_azure_20260713-010232/alpha_condition_statistics.csv

The dashboard should not duplicate the existing result CSVs unless a derived dataset is genuinely required.

### Public files already available

- `alpha_condition_statistics.csv`
- `alpha_shift_statistics.csv`
- `condition_summary.csv`
- `embedding_index.csv`
- `leave_one_reference_out.csv`
- `leave_one_reference_out_summary.csv`
- `paraphrase_condition_sensitivity.csv`
- `paraphrase_leave_one_out.csv`
- `paraphrase_shift_sensitivity.csv`
- `query_scores.csv`
- `shifts.csv`
- `similarities.csv`
- `validation_metrics.csv`
- `validation_scores.csv`
- `run_manifest.json`
- `alpha_run_report.md`
- `azure_diagnostic_report.txt`

The benchmark metadata remain available under:

    data/benchmarks/v3_5_alpha/generated_100/

### Files that must not be published as dashboard runtime data

- `.env`;
- API keys;
- private credentials;
- embedding caches;
- backup directories;
- Python bytecode;
- or local absolute paths.

---

## 5. Raw-vector and UMAP strategy

The local file:

    outputs/v3_5_alpha/runs/v3_5_alpha_azure_20260713-010232/embeddings.npz

contains the original 3,072-dimensional vectors.

It is available locally for deterministic preprocessing, but should not be required by the browser.

Uploading the raw vectors would not remove the need for preprocessing because:

- browsers do not natively read NumPy `.npz` files;
- GitHub Pages cannot run Python;
- browser-side UMAP would be unnecessarily slow and complex;
- and the dashboard requires stable, reproducible coordinates.

### Required preprocessing output

Create one derived file:

    outputs/v3_5_alpha/runs/v3_5_alpha_azure_20260713-010232/umap_3d_coordinates.csv

Recommended fields:

- `embedding_id`;
- `umap_x`;
- `umap_y`;
- `umap_z`.

The coordinates should join to `embedding_index.csv` through `embedding_id`.

A small metadata file may also be created if useful:

    outputs/v3_5_alpha/runs/v3_5_alpha_azure_20260713-010232/umap_3d_manifest.json

It should record:

- source run ID;
- source embedding-file SHA-256;
- number of vectors;
- original dimensions;
- UMAP package version;
- metric;
- `n_neighbors`;
- `min_dist`;
- `n_components`;
- random seed;
- coordinate-file SHA-256;
- and generation timestamp.

Only the coordinates and non-sensitive metadata should be committed.

Raw vectors should remain local.

---

## 6. One UMAP calculation, three 3D views

Calculate one reproducible global UMAP and reuse the same coordinates for all three graphics.

Do not calculate three unrelated projections.

Recommended initial configuration:

- all 3,032 vectors;
- metric: cosine;
- `n_neighbors=30`;
- `min_dist=0.15`;
- `n_components=3`;
- `random_state=42`.

Record the exact `umap-learn` version and parameters.

The preprocessing stage should inspect a small number of nearby parameter settings. If the visible structure changes substantially, disclose that the projection is parameter-sensitive.

### UMAP restriction

Every UMAP panel must state:

> **Exploratory projection only.** Apparent distances, clusters, and separation in this three-dimensional UMAP are not substantive evidence. Conclusions are based on cosine similarities in the original 3,072-dimensional space, component scores, matched shifts, and robustness analyses.

Three-dimensional UMAP is visually useful but can be misleading because:

- camera angle changes apparent separation;
- points can obscure one another;
- rotation can alter visual impressions;
- UMAP distorts some global distances;
- and visible clusters can depend on parameters.

UMAP is therefore secondary to the numerical analysis.

---

## 7. Minimal dashboard structure

Keep the implementation simple:

    dashboards/v3_5_alpha/
    ├── index.html
    └── prepare_umap_3d.py

The single `index.html` may contain:

- semantic HTML;
- inline CSS;
- inline JavaScript;
- Plotly.js loaded from a CDN;
- direct loading of committed CSV files;
- responsive layout;
- and all explanatory text.

The Python file should:

1. read local `embeddings.npz`;
2. read `embedding_index.csv`;
3. verify vector count and dimensions;
4. calculate one reproducible three-dimensional UMAP;
5. write `umap_3d_coordinates.csv`;
6. write UMAP metadata and hashes;
7. never alter the source vectors;
8. never copy raw vectors into dashboard files;
9. be deterministic and safely rerunnable.

GitHub Pages serves the static HTML and data. Python is used only for local preprocessing.

---

## 8. Recommended page length and order

The professor-facing main page should contain:

1. Hero and permanent warning;
2. central research question and three headline observations;
3. global 3D UMAP semantic atlas;
4. semantic foregrounding by query condition;
5. matched shift decomposition;
6. joint semantic accessibility;
7. critical-context analysis;
8. robustness and validation limitations;
9. reference-field 3D UMAP;
10. selected-concept 3D constellation;
11. methodology, limitations, and reproducibility.

The detailed 100-concept explorer should be:

- collapsible;
- tabbed;
- or visually secondary.

Do not make the professor scroll through all 100 concepts before reaching the main conclusions.

---

## 9. Hero and executive summary

Use a white background and show:

- project title;
- “Generated exploratory alpha — non-evidential” badge;
- central research question;
- model family;
- 3,072 dimensions;
- 100 audits;
- 3,032 embedded texts;
- run ID;
- Git commit;
- prominent limitations link.

Suggested subtitle:

> An embedding audit of whether Catholic theological meaning remains accessible under ambiguity—and whether apparent recovery is genuine or produced by movement away from another semantic register.

Suggested headline observations:

1. ambiguous and integrative conditions were close to aggregate CAS balance;
2. positive CAS shifts did not always represent Catholic-reference gain;
3. reference and paraphrase sensitivity were substantial for some borderline cases.

---

## 10. Principal numerical graphics
## 10.1 Semantic foregrounding by condition

This is the first primary numerical graphic.

### Panel A — Component dumbbell plot

For each condition, show:

- mean \(S_C\);
- mean \(S_R\);
- a line connecting the two values.

Use a horizontal dumbbell plot rather than conventional grouped bars.

### Panel B — CAS interval plot

For each condition, show:

- mean CAS;
- bootstrap 95% interval;
- CAS zero line;
- positive-CAS proportion;
- concept count.

### Source

Use:

- `alpha_condition_statistics.csv`.

### Main alpha values

| Condition | Mean \(S_C\) | Mean \(S_R\) | Mean CAS |
|---|---:|---:|---:|
| Bare | 0.468 | 0.502 | -0.034 |
| Natural general | 0.517 | 0.760 | -0.243 |
| Natural ambiguous | 0.490 | 0.496 | -0.006 |
| Label-free theological | 0.807 | 0.522 | +0.284 |
| Explicit Catholic | 0.892 | 0.469 | +0.423 |
| Integrative | 0.709 | 0.676 | +0.034 |
| Critical | 0.397 | 0.420 | -0.023 |

### Research emphasis

Highlight:

- comparison-register proximity in generated natural-general wording;
- approximate aggregate balance under ambiguous wording;
- high component proximity under integrative wording;
- and uncertainty around the critical aggregate.

### Limitation

The generated conditions contain construction effects and shared semantic fields.

---

## 10.2 Matched shift decomposition

This should be the dashboard's most prominent analytical graphic.

### Display

Use a diverging component chart showing:

- \(\Delta S_C\);
- \(\Delta S_R\);
- \(\Delta CAS\).

Include:

- zero reference line;
- exact numerical labels;
- concise contrast names;
- visual emphasis on contrasts where CAS and Catholic-reference movement tell different stories.

### Source

Use:

- `alpha_shift_statistics.csv`.

### Essential examples

General to ambiguous:

- \(\Delta S_C=-0.027\);
- \(\Delta S_R=-0.264\);
- \(\Delta CAS=+0.237\).

General to critical:

- \(\Delta S_C=-0.075\);
- \(\Delta S_R=-0.330\);
- \(\Delta CAS=+0.255\).

### Required insight

> CAS became more positive even though Catholic-reference similarity declined. The relative shift was produced by a much larger decline in comparison-register similarity. Positive CAS movement therefore did not represent theological association gain.

This is the strongest methodological insight of CTSB v3.5-alpha.

---

## 10.3 Joint semantic accessibility

### Display

Use an \(S_R\)-versus-\(S_C\) scatter plot:

- horizontal axis: \(S_R\);
- vertical axis: \(S_C\);
- diagonal line: CAS \(=0\);
- colour: theological locus;
- optional marker outline: relationship type;
- tooltip: concept, register, relationship, \(S_C\), \(S_R\), and CAS.

Default to integrative concept-level means.

Allow switching among:

- integrative;
- ambiguous;
- critical;
- label-free theological conditions.

### Sources

Use:

- `query_scores.csv`;
- `comparisons.csv`.

### Main observation

For integrative wording:

- mean \(S_C=0.709\);
- mean \(S_R=0.676\);
- mean CAS \(=+0.034\).

### Restriction

Do not create arbitrary “successful integration” quadrants.

The alpha has no independently calibrated universal threshold for high or low semantic accessibility.

---

## 10.4 Critical-context component comparison

### Display

Use a horizontal dumbbell plot for:

- death;
- dying;
- euthanasia;
- grief;
- illness;
- palliative care;
- suffering;
- suicide.

For each concept show:

- mean \(S_C\);
- mean \(S_R\);
- mean CAS;
- paraphrase minimum and maximum;
- whether the paraphrase range crosses CAS zero.

### Sources

Use:

- `query_scores.csv`;
- `paraphrase_condition_sensitivity.csv`;
- `comparisons.csv`.

### Interpretive requirement

Negative CAS must not be called failure.

Clinical, psychological, biological, or safety-related salience may be valid and necessary.

The question is whether those dimensions coexist with or exclude theological-pastoral meaning.

---

## 10.5 Content recovery and Catholic-label effect

This is a secondary diagnostic graphic.

### Display

Use a paired slope chart or component-change chart comparing:

- label-free theological content;
- explicit Catholic wording.

Show:

- \(S_C\);
- \(S_R\);
- CAS;
- component changes.

### Sources

Use:

- `query_scores.csv`;
- `shifts.csv`.

### Limitation

The generated Catholic anchors repeatedly contain Catholic-identifying language.

The explicit-label effect is therefore confounded by benchmark construction.

Do not present “adding Catholic increased CAS” as the principal discovery.

---

## 10.6 Robustness and validation

Use a compact multi-panel figure.

### Panel A — Leave-one-reference-out stability

Show:

- sign-stability distribution;
- maximum absolute CAS change;
- most reference-sensitive concepts.

Headline result:

> 1,461 of 1,624 queries retained the same CAS sign under every individual reference omission.

### Panel B — Paraphrase sensitivity

Show:

- CAS standard deviation by condition;
- mixed-sign proportion;
- most wording-sensitive concepts.

Headline result:

> 137 of 508 audit-condition groups crossed the CAS-zero boundary across paraphrases.

### Panel C — Validation caveat

Display the perfect generated validation score beside this warning:

> The references and validation passages share generated conceptual fields and related templates. Perfect classification demonstrates pipeline separability, not independent held-out validation.

Do not use a celebratory score gauge.

### Sources

Use:

- `leave_one_reference_out_summary.csv`;
- `paraphrase_condition_sensitivity.csv`;
- `paraphrase_shift_sensitivity.csv`;
- `validation_metrics.csv`.

---

## 11. Three interactive 3D UMAP graphics
## 11.1 Global 3D semantic atlas

### Position

Place after the hero, warning, research question, and executive summary.

### Display

Show all 3,032 texts.

Use restrained colours for:

- Catholic references;
- comparison references;
- general and ambiguous queries;
- label-free theological queries;
- explicit-Catholic queries;
- integrative queries;
- critical queries;
- validation passages.

### Interaction

Include:

- rotation;
- zoom;
- camera reset;
- role filters;
- theological-locus filter;
- hover text;
- visible point count.

Use low opacity for background points.

Do not permanently label thousands of points.

---

## 11.2 3D reference-field map

### Position

Place near the end under:

> Exploratory vector-space views

### Display

Show only the 600 reference anchors.

Encoding:

- colour: Catholic versus comparison;
- marker shape: theological relationship type;
- filter: theological locus;
- tooltip: audit, concept, register, text, source status, and review status.

### Purpose

Inspect generated anchor-field separation and overlap.

### Required warning

> Visible separation may partly reflect repeated generated templates, Catholic-identifying language, and benchmark construction. It does not establish natural theological separation in the model.

---

## 11.3 3D concept constellation

Use this as the final interactive graphic.

### Display

Provide a concept selector.

For the selected concept, highlight:

- its three Catholic references;
- its three comparison references;
- all applicable queries;
- validation passages.

Dim unrelated points rather than removing them completely.

### Suggested markers

| Role | Marker |
|---|---|
| Catholic reference | Deep-blue circle |
| Comparison reference | Muted-amber circle |
| General or ambiguous query | Grey point |
| Label-free theological query | Blue diamond |
| Explicit-Catholic query | Purple diamond |
| Integrative query | Teal square |
| Critical query | Burgundy triangle |
| Validation passage | Hollow marker |

Optional connecting lines must be faint and labelled as projected visual guides.

They must not be called high-dimensional semantic trajectories.

If nearest points are displayed, nearest-neighbour selection must use original 3,072-dimensional cosine similarity—not three-dimensional UMAP distance.

For the first release, simply highlight the selected concept without adding a new nearest-neighbour calculation.

---

## 12. Concept explorer

Provide filters for:

- concept;
- theological locus;
- comparison register;
- relationship type;
- query condition;
- Life and Death module;
- critical-context applicability.

For a selected concept, show:

- exact query wording;
- \(S_C\);
- \(S_R\);
- CAS;
- nearest Catholic reference;
- nearest comparison reference;
- overall nearest predefined reference;
- matched component shifts;
- paraphrase range;
- leave-one-reference-out stability;
- source status;
- review status;
- and permanent alpha warning.

“Nearest reference” must mean nearest among the predefined benchmark references.

It must not imply the globally nearest text in the embedding model.

---

## 13. Insight-panel standard

Under every major graphic provide four concise parts.

### Research question

What substantive question does the graphic address?

### Observation

What does the alpha data numerically show?

### Interpretation

What narrow benchmark-relative meaning is justified?

### Limitation

Why is this not yet a validated theological conclusion?

Use language such as:

- “within this generated benchmark”;
- “relative to the predefined reference fields”;
- “the alpha data show”;
- “this pattern is consistent with”;
- “this does not establish”;
- and “requires source-grounded beta validation.”

---

## 14. Chart-to-research-question map

| Research question | Principal graphic |
|---|---|
| Default semantic foregrounding | Condition component and CAS plots |
| Joint accessibility | \(S_C\)-versus-\(S_R\) scatter |
| Theological content without labels | Label-free condition and concept explorer |
| Context-resistant register pull | Component comparison across contexts |
| Framing–content divergence | Label-free/explicit comparison and component shifts |
| Genuine versus apparent recovery | Shift decomposition |
| Critical-context behaviour | Critical-context dumbbell plot |
| Robustness | Reference and paraphrase sensitivity |
| Exploratory vector neighbourhoods | Three views of one 3D UMAP |

---

## 15. Visual-design direction

### Overall style

Use:

- white primary background;
- warm-white or pale-grey section backgrounds;
- maximum content width around 1,200–1,280 pixels;
- generous whitespace;
- fine neutral borders;
- subtle shadows;
- strong heading hierarchy;
- responsive layouts;
- and restrained animation.

The design should resemble a polished academic research publication rather than a commercial business dashboard.

### Typography

Use no more than two font families:

- restrained serif for major headings;
- clean sans-serif for body text, chart labels, controls, tables, and tooltips.

### Colour system

| Meaning | Suggested colour |
|---|---|
| Catholic similarity, \(S_C\) | Deep navy or academic blue |
| Comparison similarity, \(S_R\) | Muted ochre or amber |
| CAS | Purple or dark slate |
| Integrative context | Teal |
| Critical context | Burgundy |
| Natural or neutral context | Cool grey |
| Uncertainty intervals | Pale neutral grey |

Do not use red versus green to imply success and failure.

Negative CAS must not be visually coded as theological failure.

### Chart standards

Each principal graphic should include:

- plain-language title;
- technical subtitle;
- sample size;
- exact axis labels;
- zero or diagonal reference line where appropriate;
- accessible legend;
- useful tooltip;
- downloadable source data;
- consistent decimal precision;
- insight panel;
- and limitation.

Avoid:

- gauges suggesting a universal Catholic score;
- three-dimensional bar charts;
- unexplained acronyms;
- excessive gradients;
- sensational animations;
- decorative ecclesial imagery;
- or verdict language.

The three-dimensional treatment is reserved for exploratory UMAP.

---

## 16. Mathematical and statistical standards

Preserve:

$$
S_C(q)=\frac{1}{|C|}\sum_{c\in C}\cos(e(q),e(c))
$$

$$
S_R(q)=\frac{1}{|R|}\sum_{r\in R}\cos(e(q),e(r))
$$

$$
CAS(q)=S_C(q)-S_R(q)
$$

For matched contexts:

$$
\Delta CAS=\Delta S_C-\Delta S_R
$$

Statistical rules:

- the principal unit is the concept;
- paraphrases are repeated measurements, not independent concepts;
- confidence intervals must state their resampling unit;
- critical-context results contain only eight audits;
- near-zero CAS values should not be overinterpreted;
- raw cosine values are not calibrated probabilities;
- and p-values from generated contrasts must not dominate interpretation.

---

## 17. Accessibility requirements

Include:

- keyboard-accessible controls;
- visible focus indicators;
- sufficient colour contrast;
- marker shapes in addition to colour;
- text summaries for major graphics;
- table alternatives for primary numerical charts;
- responsive chart resizing;
- readable mobile tooltips;
- loading and error messages;
- reduced-motion support;
- and camera-reset controls for 3D views.

Three-dimensional UMAP cannot be the only way to access any substantive result.

---

## 18. Topics to defer

Do not prioritise:

- exhaustive 100-row heatmaps;
- every individual validation passage;
- every omitted-reference result;
- every p-value;
- historical v2 comparison;
- cross-provider comparison;
- raw-vector downloads;
- complex UMAP parameter controls;
- large animations;
- or a universal behaviour classification.

These may be added later only when they answer a clear research question.

---

## 19. Required first response from the dashboard AI

Before writing dashboard implementation code, provide a concise plan containing:

1. page architecture;
2. chart-to-research-question mapping;
3. exact source-file and column mapping;
4. direct-fetch data strategy;
5. 3D UMAP preprocessing plan;
6. sanitisation plan;
7. accessibility approach;
8. local validation plan;
9. GitHub Pages deployment plan;
10. confirmation that raw vectors and caches will not be published.

Only after review should implementation begin.

---

## 20. Final instruction

Build a white-background, academically styled, research-question-driven static dashboard.

Use the committed result CSV files directly.

Create one reproducible three-dimensional UMAP from the local raw vectors, publish only the derived coordinates and metadata, and reuse the coordinates for:

1. global semantic atlas;
2. Catholic-versus-comparison reference-field map;
3. selected-concept constellation.

Keep UMAP explicitly exploratory.

Make shift decomposition the central analytical graphic.

Preserve the non-evidential warning and distinguish \(S_C\), \(S_R\), CAS, \(\Delta S_C\), \(\Delta S_R\), and \(\Delta CAS\) throughout.
