# New-thread prompt: CTSB v3.5-alpha visualisation dashboard

You are building a professional static data-visualisation dashboard for the project:

> **Vector Space and Theological Meaning**

The dashboard concerns:

> **CTSB v3.5-alpha — Generated Exploratory 100-Concept Results**

Before proposing or making changes, read all material in the supplied dashboard context bundle.

## 1. Immediate task

Build a professional, responsive, accessible static dashboard for the completed CTSB v3.5-alpha Azure development run.

The site must be created at:

    dashboards/v3_5_alpha/

The expected public URL is:

    https://yin-renlong.github.io/vector-space-theological-meaning/dashboards/v3_5_alpha/

Do not replace the root `index.html`. It remains a compatibility copy of the historical v2 dashboard.

## 2. Evidential status

The dashboard must be labelled prominently and repeatedly as:

> **Generated exploratory alpha — non-evidential**

The alpha references, queries, and validation passages were generated for instrument development.

They are:

- unreviewed;
- not verified quotations;
- not verified paraphrases;
- not verified source summaries;
- and not a final source-grounded benchmark.

The development-validation passages were constructed from the same conceptual fields as the references. The perfect validation score is therefore a pipeline diagnostic, not independent held-out validation.

The dashboard must not present the alpha results as evidence that:

- Catholic theology is true or false;
- the model is Catholic or anti-Catholic;
- the model has beliefs, intentions, a subconscious, or hostility;
- the model deliberately deceives users;
- the model is pastorally adequate or inadequate;
- a chatbot produced a doctrinally correct or incorrect answer;
- or the results generalise to all embedding models.

Use benchmark-relative language.

## 3. Central interpretive rule

Always display and interpret these separately:

- Catholic-reference mean similarity, \(S_C\);
- comparison-reference mean similarity, \(S_R\);
- Catholic Association Contrast, \(CAS=S_C-S_R\).

For shifts, display:

- \(\Delta S_C\);
- \(\Delta S_R\);
- \(\Delta CAS\).

A positive \(\Delta CAS\) must never automatically be called theological recovery.

The dashboard must explicitly show that:

- general-to-ambiguous wording produced positive \(\Delta CAS\) while \(S_C\) declined;
- general-to-critical wording produced positive \(\Delta CAS\) while \(S_C\) declined.

These are examples of apparent relative recovery without Catholic-reference association gain.

## 4. Research emphasis

The principal research problem is not the predictable fact that adding Catholic vocabulary moves a query toward Catholic references.

The important questions are:

1. Which register is foregrounded under natural ambiguity?
2. Can Catholic theological and valid adjacent meanings remain jointly accessible?
3. Is theological substance legible without an overt Catholic label?
4. Does another semantic register remain influential under Catholic framing?
5. Does Catholic surface framing correspond to substantive Catholic-reference recovery?
6. Is apparent recovery caused by actual \(S_C\) gain or only \(S_R\) decline?
7. What happens under critical or crisis language?
8. Which results are sensitive to paraphrases or exact reference selection?
9. Where might theological framing and semantic content diverge?
10. What can and cannot be concluded from a generated alpha benchmark?

## 5. Data-location rule

The completed Azure outputs currently exist locally under:

    outputs/v3_5_alpha/runs/v3_5_alpha_azure_20260713-010232/

That directory is intentionally ignored by Git.

A GitHub Pages browser cannot fetch ignored local output files.

Therefore, create a deterministic Python data-preparation script that:

1. reads the local source benchmark and Azure result files;
2. selects only the fields needed by the dashboard;
3. removes local filesystem paths and unnecessary deployment details;
4. converts selected data into compact CSV or JSON files;
5. writes those public files under:

       dashboards/v3_5_alpha/data/

6. generates a sanitised `dashboard_manifest.json`;
7. preserves the alpha evidential warning;
8. records source-file hashes where useful;
9. never copies `.env`, credentials, caches, raw vectors, or local paths;
10. can be safely rerun.

The tracked dashboard must read only files available inside the GitHub repository.

Do not make browser code attempt to fetch from `/Users/...` or from ignored `outputs/`.

## 6. Data publication policy

### Publish or derive from these core files

Benchmark metadata:

- `data/benchmarks/v3_5_alpha/generated_100/comparisons.csv`
- `data/benchmarks/v3_5_alpha/generated_100/references.csv`
- `data/benchmarks/v3_5_alpha/generated_100/queries.csv`

Core aggregate results:

- `alpha_condition_statistics.csv`
- `alpha_shift_statistics.csv`
- `validation_metrics.csv`

Core concept and query results:

- `query_scores.csv`
- `shifts.csv`

Core robustness summaries:

- `leave_one_reference_out_summary.csv`
- `paraphrase_condition_sensitivity.csv`
- `paraphrase_shift_sensitivity.csv`

Optional detail:

- selected fields from `validation_scores.csv`;
- selected fields from `similarities.csv` only if genuinely required for a reference-level explorer.

### Do not publish

- `embeddings.npz`;
- embedding caches;
- `.env`;
- API keys;
- endpoints;
- local absolute paths;
- `_patch_backups/`;
- `ai_context/`;
- Python bytecode;
- raw output directories as a whole;
- unsanitised manifests or reports.

Do not publish `embedding_index.csv` unless a specific reproducibility feature requires it.

The dashboard does not need raw vectors. Substantive charts must use the scored high-dimensional results already produced.

## 7. Required site structure

Use a professional static structure:

    dashboards/v3_5_alpha/
    ├── index.html
    ├── README.md
    ├── prepare_dashboard_data.py
    ├── assets/
    │   ├── css/
    │   │   └── styles.css
    │   └── js/
    │       └── dashboard.js
    └── data/
        ├── dashboard_manifest.json
        ├── condition_statistics.json
        ├── shift_statistics.json
        ├── concepts.json
        ├── query_scores.json
        ├── shifts.json
        ├── validation_summary.json
        ├── reference_sensitivity.json
        └── paraphrase_sensitivity.json

The exact derived filenames may be adjusted if there is a clear reason, but keep the implementation lean.

Use:

- semantic HTML5;
- responsive CSS;
- accessible colours and labels;
- keyboard-accessible controls;
- CSS variables;
- minimal JavaScript;
- no build step;
- Plotly.js or another lightweight browser chart library;
- and clear loading/error states.

The dashboard must work through:

    python3 -m http.server 8000

Because the page fetches data files, local testing should use an HTTP server rather than relying only on `file://`.

## 8. Required dashboard sections

### 8.1 Hero and permanent warning

Show:

- CTSB v3.5-alpha;
- generated exploratory dashboard;
- non-evidential status;
- model family;
- 3,072 dimensions;
- 100 audits;
- 3,032 embedded texts;
- Git commit;
- run ID;
- and a visible limitations link.

Do not expose the Azure endpoint, API key, local path, or unnecessary deployment metadata.

### 8.2 Research questions

Present a concise version of the central research problem:

- semantic foregrounding under ambiguity;
- joint accessibility;
- theological legibility without labels;
- context-resistant register pull;
- theological framing–content divergence;
- genuine versus apparent recovery;
- critical-context behaviour;
- persistent attenuation hypotheses;
- and robustness.

### 8.3 Condition overview

Create a chart showing, for every condition:

- mean \(S_C\);
- mean \(S_R\);
- mean CAS;
- bootstrap interval for CAS;
- positive-CAS proportion.

Conditions:

- bare;
- natural general;
- natural ambiguous;
- label-free theological;
- explicit Catholic;
- integrative;
- critical.

Below the graphic, add a concise evidence-aware insight panel.

It must state that the strong general, theological, and explicit-Catholic separation is affected by benchmark construction.

### 8.4 Shift decomposition

Create a component-level chart showing:

- \(\Delta S_C\);
- \(\Delta S_R\);
- \(\Delta CAS\).

Emphasise:

- general to ambiguous;
- general to critical;
- general to label-free theological;
- label-free theological to explicit Catholic;
- general to integrative.

Below the chart, explain why positive \(\Delta CAS\) can be misleading without positive \(\Delta S_C\).

This is the central methodological visualisation.

### 8.5 Concept explorer

Provide filters for:

- concept;
- theological locus;
- comparison register;
- relationship type;
- condition;
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
- leave-one-reference-out stability;
- paraphrase range;
- source/review warning.

“Nearest reference” must always mean nearest among the predefined benchmark references, not globally nearest text in the model.

### 8.6 Integrative accessibility

Create an \(S_C\)-versus-\(S_R\) scatter plot for integrative queries.

Avoid arbitrary universal success thresholds.

Describe the chart as relative component accessibility.

Do not claim that high scores prove theological integration.

### 8.7 Critical-context analysis

Display the eight critical audits:

- death;
- dying;
- euthanasia;
- grief;
- illness;
- palliative care;
- suffering;
- suicide.

Show \(S_C\), \(S_R\), CAS, and paraphrase range.

Do not describe negative CAS as failure.

Explain that clinical, biological, or psychological salience may be valid and safety-relevant.

### 8.8 Label-free versus explicit Catholic

Compare:

- label-free theological content;
- explicit Catholic framing.

Show both component scores and their changes.

State clearly that the alpha label effect is confounded by repeated Catholic-identifying language in generated Catholic references.

Do not present “adding Catholic increased CAS” as the principal discovery.

### 8.9 Robustness

Visualise:

- leave-one-reference-out sign stability;
- maximum CAS change after omitting a reference;
- paraphrase CAS standard deviation;
- mixed-sign paraphrase groups;
- the most reference-sensitive concepts;
- and the most wording-sensitive concepts.

Include the observed alpha summaries:

- 1,461 of 1,624 queries were sign-stable under every reference omission;
- 137 of 508 audit-condition groups contained mixed CAS signs across paraphrases.

### 8.10 Validation and construction leakage

Show the generated validation result, but do not celebrate the perfect score.

Place beside it a clear explanation:

> The validation passages and references share generated conceptual fields and related templates. The score demonstrates pipeline separability, not independent validation.

### 8.11 Methodology and reproducibility

Include:

- CAS definition;
- shift decomposition;
- model and dimensions;
- benchmark counts;
- run ID;
- Git commit;
- evidence restrictions;
- links to the repository methodology;
- and downloadable public dashboard data.

## 9. Insights beneath graphics

Every major graphic must include an insight panel with four parts:

1. **Question:** what research question the chart addresses;
2. **Observation:** what the displayed alpha data numerically show;
3. **Interpretation:** the narrow benchmark-relative meaning;
4. **Limitation:** why the observation is not yet a validated theological conclusion.

Do not generate exaggerated or causal claims.

Use phrases such as:

- “within this generated benchmark”;
- “relative to the predefined reference fields”;
- “the alpha data show”;
- “this pattern is consistent with”;
- “this does not establish”;
- and “requires source-grounded beta validation.”

## 10. Design direction

Use a restrained, professional research-dashboard style.

Suggested qualities:

- academic rather than promotional;
- high contrast and accessible;
- spacious layout;
- strong typographic hierarchy;
- restrained theological colours such as deep blue, burgundy, muted gold, and neutral greys;
- consistent Catholic/comparison/component colours;
- tooltips with exact values;
- explanatory subtitles;
- downloadable chart data;
- and responsive layouts for desktop, tablet, and mobile.

Avoid:

- decorative ecclesial imagery;
- sensational red/green success framing;
- gauges suggesting a universal Catholic score;
- unexplained acronyms;
- three-dimensional charts;
- UMAP;
- raw-vector projections;
- or visual language implying doctrinal grading.

## 11. Required safeguards

Before committing:

1. validate every public data file;
2. scan dashboard files for `/Users/`, `.env`, API keys, and Azure endpoints;
3. verify no `embeddings.npz` or cache is staged;
4. verify all data paths work under the GitHub Pages subdirectory;
5. run a local HTTP preview;
6. check responsive layout;
7. check keyboard navigation;
8. check chart fallback and loading messages;
9. run `git diff --check`;
10. print all staged files before committing.

## 12. GitHub workflow

Use:

- the existing repository;
- branch `main`;
- HTTPS origin;
- `gh` CLI;
- timestamped backups;
- deterministic Python preprocessing;
- explicit staging;
- validation before commit;
- and GitHub Pages from `main` at `/`.

Do not commit the ignored `outputs/` directory.

Commit only the dashboard implementation and its deliberately curated public data.

## 13. Response format

When implementing the dashboard:

- provide one complete copy-paste Bash block per step;
- begin each block with `bash <<'BASH'` and `set -euo pipefail`;
- use timestamped backups;
- use Python `pathlib`, `shutil`, and deterministic replacement/generation;
- do not ask for manual editing;
- do not expose secrets;
- print the local preview URL, public URL, changed files, and Git status;
- and keep the implementation static and lean.

## 14. First action in the new thread

Before writing dashboard code:

1. inspect the supplied context bundle;
2. confirm the exact source files and their schemas;
3. briefly propose the dashboard architecture and chart-to-data mapping;
4. identify which output columns will be published;
5. identify which output columns will be removed or sanitised;
6. then provide the implementation command.

Do not request raw vectors or secrets.
