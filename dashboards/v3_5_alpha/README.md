# CTSB v3.5-alpha Dashboard

A static, research-first visualisation of the completed CTSB v3.5-alpha
100-concept Azure development run.

## Public dashboard

https://yin-renlong.github.io/vector-space-theological-meaning/dashboards/v3_5_alpha/

## Local preview

From the repository root, run:

    /opt/homebrew/bin/python3 -m http.server 8000

Then open:

    http://localhost:8000/dashboards/v3_5_alpha/

The dashboard fetches committed CSV and JSON files, so it should be tested
through HTTP rather than file://.

## Structure

    dashboards/v3_5_alpha/
    ├── index.html
    ├── README.md
    ├── prepare_umap_3d.py
    ├── requirements-umap.txt
    └── assets/
        ├── css/styles.css
        └── js/dashboard.js

## Data strategy

The dashboard fetches selected committed result tables directly from:

    outputs/v3_5_alpha/runs/v3_5_alpha_azure_20260713-010232/

Benchmark metadata are fetched directly from:

    data/benchmarks/v3_5_alpha/generated_100/

Complete result tables are not duplicated in the dashboard directory.

## UMAP preprocessing

The preprocessing script reads the local embeddings.npz file and creates one
reproducible three-dimensional UMAP with:

- cosine metric;
- 30 neighbours;
- minimum distance 0.15;
- three components;
- random seed 42;
- all 3,032 vectors.

Only the derived coordinates and non-sensitive preprocessing manifest are
published. The same coordinates power all three interactive UMAP views.

To recreate the projection using Python 3.11:

    /opt/homebrew/bin/python3 -m venv .dashboard-venv
    .dashboard-venv/bin/python -m pip install -r dashboards/v3_5_alpha/requirements-umap.txt
    .dashboard-venv/bin/python dashboards/v3_5_alpha/prepare_umap_3d.py --diagnostics

Raw vectors and caches are not browser runtime data.

## Main visualisations

- global three-dimensional semantic atlas;
- condition-level component and CAS analysis;
- matched delta S_C, delta S_R, and delta CAS decomposition;
- joint component accessibility scatter;
- critical-context component comparison;
- label-free versus explicit-Catholic diagnostic;
- reference and paraphrase sensitivity;
- generated-validation construction caveat;
- reference-field UMAP;
- selected-concept UMAP constellation;
- detailed 100-concept explorer.

The numerical cosine analysis in the original 3,072-dimensional space remains
primary. UMAP is exploratory.
