# CTSB v3.5-alpha Dashboard Design

## 1. Dashboard identity

**Project:** Vector Space and Theological Meaning  
**Dashboard:** CTSB v3.5-alpha Generated Exploratory Results  
**Azure run:** `v3_5_alpha_azure_20260713-010232`  
**Public status:** Generated, unreviewed, exploratory, and non-evidential

The dashboard should provide a professional visual explanation of the CTSB v3.5-alpha Azure experiment.

It should be suitable for presentation to a university professor while remaining:

- mathematically accurate;
- statistically responsible;
- methodologically clear;
- informed by NLP and embedding-evaluation practice;
- visually elegant;
- concise enough to understand in one sitting;
- and explicit about the limitations of the generated benchmark.

The dashboard must not present the alpha as a validated theological audit.

---

## 2. Central research narrative

The dashboard should be designed around this central question:

> **Does Catholic theological meaning remain accessible under ambiguity and semantic competition, and can apparent theological recovery be distinguished from genuine Catholic-reference association gain?**

The page should tell one coherent story:

1. What semantic register is foregrounded under natural or ambiguous language?
2. Can Catholic theological and valid adjacent meanings remain jointly accessible?
3. Is theological substance legible without an overt Catholic label?
4. Does explicit Catholic framing produce substantive theological recovery?
5. Can CAS become more positive even while Catholic-reference similarity declines?
6. What happens under critical and crisis language?
7. How sensitive are the results to paraphrases and exact reference selection?

The predictable fact that adding Catholic vocabulary increases Catholic association must not become the dashboard's main conclusion.

---

## 3. Evidential warning

Display this warning prominently near the top and repeat a shorter version near the conclusion:

> **Generated exploratory alpha — non-evidential.** The references, queries, and validation passages were generated for instrument development and have not received exact-source, theological, disciplinary, or independent validation review. Results are relative to the predefined generated reference fields and must not be interpreted as validated findings about Catholic theology, model bias, pastoral adequacy, or ChatGPT responses.

The dashboard must not imply:

- that CAS is a Catholic truth score;
- that negative CAS means hostility, error, or secularism;
- that positive CAS proves theological adequacy;
- that the embedding model has beliefs, intentions, consciousness, or a subconscious;
- that the model intentionally deceives users;
- or that these findings generalise to all AI systems.

---

## 4. Public data location

The dashboard may read the committed result files directly from:

    ../../outputs/v3_5_alpha/runs/v3_5_alpha_azure_20260713-010232/

when the dashboard is located at:

    dashboards/v3_5_alpha/index.html

For example:

    ../../outputs/v3_5_alpha/runs/v3_5_alpha_azure_20260713-010232/alpha_condition_statistics.csv

This preserves the existing project structure and avoids duplicating the result tables.

The browser may directly fetch these tracked CSV and JSON files through GitHub Pages.

Do not publish or request:

- `embeddings.npz`;
- `embedding_cache.json`;
- `.env`;
- API keys;
- private credentials;
- or backup files.

`embedding_index.csv` may be published because it provides text-role metadata needed for UMAP tooltips and reproducibility.

---

## 5. Required static dashboard location

Create the dashboard under:

    dashboards/v3_5_alpha/
    ├── index.html
    ├── README.md
    └── assets/
        ├── css/
        │   └── styles.css
        └── js/
            └── dashboard.js

A small local UMAP-preparation script may also be added:

    dashboards/v3_5_alpha/prepare_umap.py

Generated public UMAP coordinates may be stored as:

    outputs/v3_5_alpha/runs/v3_5_alpha_azure_20260713-010232/umap_coordinates.csv

or, if implementation simplicity requires it:

    dashboards/v3_5_alpha/data/umap_coordinates.csv

Only two-dimensional coordinates and sanitised metadata should be published. Raw vectors must remain local.

Expected public dashboard URL:

    https://yin-renlong.github.io/vector-space-theological-meaning/dashboards/v3_5_alpha/

---

## 6. Recommended page length and order

The main page should contain approximately eight analytical sections:

1. Hero, warning, and executive summary;
2. global exploratory UMAP;
3. semantic foregrounding by query condition;
4. matched shift decomposition;
5. joint accessibility;
6. critical-context analysis;
7. robustness and validation limitations;
8. final exploratory UMAP views and methodology.

The complete 100-concept explorer should be:

- collapsible;
- tabbed;
- or visually secondary.

Do not display all 100 concepts in one long unstructured page.

---

## 7. Visual design direction

### 7.1 Overall style

Use a restrained academic visual style:

- white primary background;
- warm-white or very pale grey section backgrounds;
- maximum content width of approximately 1,200–1,280 pixels;
- generous whitespace;
- fine neutral borders;
- very subtle shadows;
- clear vertical rhythm;
- strong heading hierarchy;
- and responsive layouts.

The design should feel like a professional research publication rather than a commercial analytics product.

### 7.2 Typography

Use no more than two font families:

- a restrained serif for the project title and major section headings;
- a clean sans-serif for body text, chart labels, controls, tables, and tooltips.

Typography must remain readable on laptops, tablets, and phones.

### 7.3 Colour system

Use a consistent colour-blind-aware palette:

| Meaning | Suggested colour |
|---|---|
| Catholic similarity, \(S_C\) | Deep navy or academic blue |
| Comparison similarity, \(S_R\) | Muted ochre or amber |
| CAS | Purple or dark slate |
| Integrative context | Teal |
| Critical context | Burgundy |
| Natural or neutral context | Cool grey |
| Uncertainty intervals | Light neutral grey |

Do not use red versus green to imply failure and success.

Negative CAS must not be visually coded as theological failure.

### 7.4 Chart standards

Every principal graphic should include:

- a plain-language title;
- a technical subtitle;
- sample size;
- exact axis labels;
- a zero or diagonal reference line where appropriate;
- an accessible legend;
- useful tooltips;
- downloadable source data;
- consistent decimal precision;
- and an insight panel immediately underneath.

Use three decimal places in charts and four where additional precision is genuinely useful.

Avoid:

- three-dimensional charts;
- decorative gauges;
- universal “Catholic score” indicators;
- unexplained acronyms;
- sensational animation;
- excessive gradients;
- ecclesial decoration unrelated to the evidence;
- and red/green verdict language.

---

## 8. Insight-panel standard

Under every major graphic, provide four concise elements:

### Research question

What substantive research question does the chart address?

### Observation

What does the alpha data numerically show?

### Interpretation

What narrow benchmark-relative interpretation is justified?

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

# 9. Principal graphics

## 9.1 Graphic 1 — Global exploratory UMAP

### Position

Place it after the hero, warning, and short executive summary.

Do not place it above the evidential warning.

### Purpose

Provide an attractive visual orientation to the complete generated embedding set.

It must not establish a substantive result.

### Data

Locally read:

- `embeddings.npz`;
- `embedding_index.csv`;
- benchmark query, reference, and validation metadata.

Publish only:

- UMAP x coordinate;
- UMAP y coordinate;
- text identifier;
- text role;
- audit ID;
- concept;
- condition or group;
- theological locus;
- relationship type;
- short text or tooltip text.

### Display

Show all 3,032 embedded texts using restrained role-based colours:

- Catholic references;
- comparison references;
- natural and ambiguous queries;
- label-free theological queries;
- explicit-Catholic queries;
- integrative queries;
- critical queries;
- validation passages.

Use low opacity for background points and clearer highlighting on hover or selection.

### Required caption

> This is an exploratory two-dimensional projection of 3,072-dimensional vectors. UMAP can preserve some local neighbourhood structure but may distort global distances, cluster shapes, and apparent separation. Substantive conclusions rely on high-dimensional cosine similarities, component scores, matched shifts, validation, and sensitivity analysis—not visual position alone.

---

## 9.2 Graphic 2 — Semantic foregrounding by condition

This is the first primary numerical graphic.

### Panel A: component dumbbell plot

For each query condition, show:

- mean \(S_C\);
- mean \(S_R\);
- a line connecting the two values.

A horizontal dumbbell plot is preferred over ordinary grouped bars because it highlights the relationship between the component similarities.

### Panel B: CAS interval plot

For each condition, show:

- mean CAS;
- bootstrap 95% interval;
- CAS zero line;
- positive-CAS proportion;
- concept count.

### Data

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

- strong comparison proximity in the generated natural-general condition;
- approximate aggregate balance under ambiguous wording;
- simultaneous high component proximity under integrative wording;
- and uncertainty around the small critical-context aggregate.

### Limitation

The generated conditions contain construction effects and shared semantic fields.

---

## 9.3 Graphic 3 — Matched shift decomposition

This should be the most prominent analytical graphic.

### Display

Use a diverging component chart showing, for each contrast:

- \(\Delta S_C\);
- \(\Delta S_R\);
- \(\Delta CAS\).

Include:

- a zero line;
- exact numerical labels;
- concise contrast names;
- and highlighting for contrasts where CAS and Catholic-reference movement tell different stories.

### Data

Use:

- `alpha_shift_statistics.csv`.

### Essential examples

#### General to ambiguous

- \(\Delta S_C=-0.027\);
- \(\Delta S_R=-0.264\);
- \(\Delta CAS=+0.237\).

#### General to critical

- \(\Delta S_C=-0.075\);
- \(\Delta S_R=-0.330\);
- \(\Delta CAS=+0.255\).

### Required insight

> CAS became more positive even though Catholic-reference similarity declined. The relative shift was produced by a much larger decline in comparison-register similarity. Positive CAS movement therefore did not represent theological association gain.

This is the strongest methodological insight of CTSB v3.5-alpha.

---

## 9.4 Graphic 4 — Joint semantic accessibility

### Display

Use an \(S_R\)-versus-\(S_C\) scatter plot:

- horizontal axis: \(S_R\);
- vertical axis: \(S_C\);
- diagonal line: CAS \(=0\);
- colour: theological locus;
- optional shape or border: relationship type;
- tooltip: concept, comparison register, relationship, \(S_C\), \(S_R\), and CAS.

Default to integrative concept-level means.

Allow optional switching among:

- integrative;
- ambiguous;
- critical;
- and label-free theological conditions.

### Data

Use:

- `query_scores.csv`;
- `comparisons.csv`.

### Main alpha observation

For integrative wording:

- mean \(S_C=0.709\);
- mean \(S_R=0.676\);
- mean CAS \(=+0.034\).

### Statistical restriction

Do not create arbitrary “successful integration” thresholds.

The current alpha has no independently calibrated universal high/low cosine boundary.

---

## 9.5 Graphic 5 — Critical-context component comparison

### Display

Use a horizontal paired-dot or dumbbell plot for:

- death;
- dying;
- euthanasia;
- grief;
- illness;
- palliative care;
- suffering;
- suicide.

For every concept, show:

- mean \(S_C\);
- mean \(S_R\);
- mean CAS;
- paraphrase minimum and maximum;
- whether paraphrases cross the CAS-zero line.

### Data

Use:

- `query_scores.csv`;
- `paraphrase_condition_sensitivity.csv`;
- `comparisons.csv`.

### Interpretive requirement

Negative CAS must not be called failure.

Clinical, psychological, biological, or safety-related salience may be valid.

The research question is whether these dimensions coexist with or exclude theological-pastoral meaning.

---

## 9.6 Graphic 6 — Content recovery and Catholic-label effect

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

### Data

Use:

- `query_scores.csv`;
- `shifts.csv`.

### Required limitation

The generated Catholic anchors repeatedly contain Catholic-identifying wording.

The explicit-label effect is therefore confounded by benchmark construction.

Do not present “adding Catholic increased CAS” as the principal discovery.

---

## 9.7 Graphic 7 — Robustness

Use a compact multi-panel figure.

### Panel A: leave-one-reference-out stability

Show:

- sign-stability distribution;
- maximum absolute CAS change;
- most reference-sensitive concepts.

Headline result:

> 1,461 of 1,624 queries retained the same CAS sign under every individual reference omission.

### Panel B: paraphrase sensitivity

Show:

- CAS standard deviation by condition;
- mixed-sign proportion;
- most wording-sensitive concepts.

Headline result:

> 137 of 508 audit-condition groups crossed the CAS-zero boundary across paraphrases.

### Panel C: validation caveat

Display the generated validation score alongside this warning:

> The references and validation passages share generated conceptual fields and related templates. Perfect classification demonstrates pipeline separability, not independent held-out validation.

Do not use a celebratory score gauge.

### Data

Use:

- `leave_one_reference_out_summary.csv`;
- `paraphrase_condition_sensitivity.csv`;
- `paraphrase_shift_sensitivity.csv`;
- `validation_metrics.csv`.

---

# 10. Three UMAP views

## 10.1 One computation, three views

Calculate one reproducible global UMAP and reuse the same coordinates for all three graphics.

Do not compute three unrelated projections.

Recommended initial configuration:

- metric: cosine;
- `n_neighbors=30`;
- `min_dist=0.15`;
- fixed `random_state=42`;
- all 3,032 vectors;
- record Python and `umap-learn` versions.

The preprocessing report should record:

- input vector count;
- original dimensions;
- UMAP parameters;
- random seed;
- source run ID;
- and coordinate-file hash.

The UMAP should be tested with a few nearby parameter settings. If visible structure changes substantially, disclose that the projection is parameter-sensitive.

## 10.2 UMAP view 1 — Global semantic atlas

Location: near the beginning.

Display:

- all texts;
- broad role-based colours;
- filters for locus and role;
- restrained opacity;
- rich tooltips.

Purpose:

- visual orientation;
- local-neighbourhood exploration;
- introduction to the semantic material.

## 10.3 UMAP view 2 — Reference-field map

Location: near the end under “Exploratory vector-space views.”

Display only the 600 reference points.

Encoding:

- colour: Catholic versus comparison;
- shape: relationship type;
- filter or facet: theological locus;
- tooltip: audit, concept, register, text, and review status.

Purpose:

- inspect generated anchor-field separation and overlap.

Required warning:

> Visible reference separation may reflect repeated generated templates, labels, and construction choices.

## 10.4 UMAP view 3 — Local concept-neighbourhood explorer

Location: final visual section.

Provide a concept selector.

For the selected concept, highlight:

- Catholic references;
- comparison references;
- queries by condition;
- validation passages;
- nearby points from other concepts where helpful.

Suggested markers:

| Role | Marker |
|---|---|
| Catholic reference | Deep-blue circle |
| Comparison reference | Amber circle |
| General or ambiguous query | Grey or teal point |
| Label-free theological query | Blue diamond |
| Explicit-Catholic query | Purple diamond |
| Integrative query | Teal square |
| Critical query | Burgundy triangle |
| Validation passage | Hollow marker |

Optional connecting lines between matched conditions must be faint and described as projected visual guides—not high-dimensional semantic trajectories.

---

## 11. Concept explorer

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
- and the permanent alpha warning.

“Nearest reference” must always mean nearest among the predefined benchmark references.

It must not imply the globally nearest sentence in the embedding model.

---

## 12. Chart-to-research-question map

| Research question | Principal graphic |
|---|---|
| Default semantic foregrounding | Condition component and CAS plots |
| Joint accessibility | \(S_C\)-versus-\(S_R\) scatter |
| Theological content without labels | Label-free condition and concept explorer |
| Context-resistant register pull | Component comparison across contexts |
| Framing–content divergence | Label-free/explicit comparison plus component shifts |
| Genuine versus apparent recovery | Shift decomposition |
| Critical-context behaviour | Eight-concept critical plot |
| Robustness | Reference and paraphrase sensitivity |
| Local vector neighbourhoods | Three exploratory UMAP views |

---

## 13. Mathematical and statistical standards

The dashboard must preserve:

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

Statistical standards:

- the principal unit is the concept;
- paraphrases are repeated measurements, not independent concepts;
- confidence intervals must state their resampling unit;
- critical-context results contain only eight audits;
- near-zero CAS values should not be overinterpreted;
- raw cosine values are not universal calibrated probabilities;
- and p-values from generated contrasts must not dominate the interpretation.

---

## 14. Topics to defer from the first release

Do not prioritise:

- exhaustive 100-row heatmaps;
- every validation passage;
- every omitted-reference result;
- every p-value;
- all historical v2 comparisons;
- cross-provider comparisons;
- raw-vector downloads;
- complex UMAP controls;
- large animated transitions;
- or a universal behaviour classification.

These can be added later if they answer a clear research question.

---

## 15. Accessibility and responsive requirements

The dashboard must include:

- keyboard-accessible controls;
- visible focus indicators;
- sufficient colour contrast;
- non-colour encodings where possible;
- text alternatives for major graphics;
- responsive chart resizing;
- readable mobile tooltips;
- loading and error messages;
- reduced-motion support;
- and table alternatives for central charts.

---

## 16. Implementation principles

Use:

- semantic HTML5;
- responsive CSS;
- CSS variables;
- minimal JavaScript;
- a static chart library such as Plotly.js;
- CSV parsing in the browser where practical;
- and no build step.

The site should work with:

    python3 -m http.server 8000

Then open:

    http://localhost:8000/dashboards/v3_5_alpha/

Do not fetch data from local absolute paths.

Use repository-relative paths.

---

## 17. Required first response from the dashboard AI

Before writing implementation code, the next AI should provide a concise plan containing:

1. page architecture;
2. chart-to-research-question mapping;
3. exact source file and column mapping;
4. direct-fetch data strategy;
5. UMAP preprocessing plan;
6. sanitisation plan;
7. accessibility approach;
8. local validation plan;
9. GitHub Pages deployment plan;
10. explicit confirmation that raw vectors and caches will not be published.

Only after that review should it provide the implementation command.

---

## 18. New-thread instruction

Tell the next AI:

> Read this design README and the CTSB v3.5-alpha dashboard context before proposing changes. Build a white-background, academically styled, research-question-driven static dashboard. Use the existing committed output files directly where practical. Add three views of one reproducible UMAP projection, but keep UMAP explicitly exploratory. Make shift decomposition the central analytical graphic. Preserve the non-evidential alpha warning and distinguish \(S_C\), \(S_R\), CAS, \(\Delta S_C\), \(\Delta S_R\), and \(\Delta CAS\) throughout.
