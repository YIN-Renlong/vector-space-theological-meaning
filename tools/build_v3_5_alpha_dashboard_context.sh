#!/usr/bin/env bash
set -euo pipefail

PROJECT="/Users/Renlong/Projects/GitHub/YIN-Renlong/vector-space-theological-meaning"
OUT_DIR="$PROJECT/ai_context"
DEFAULT_RUN_DIR="$PROJECT/outputs/v3_5_alpha/runs/v3_5_alpha_azure_20260713-010232"
RUN_DIR="$DEFAULT_RUN_DIR"
STAMP="$(date +%Y%m%d-%H%M%S)"
PROFILE="lean"
WITH_CODE=0
WITH_FULL_DATA=0
COPY_TO_CLIPBOARD=1
SAMPLE_ROWS=3

usage() {
  cat <<'USAGE'
Usage:
  ./tools/build_v3_5_alpha_dashboard_context.sh [options]

Options:
  --with-code
      Include the v3.5-alpha generator, v3.4 engine, and tests.

  --full-data
      Include the complete selected textual CSV files. This can create a very
      large context bundle and is normally unnecessary.

  --sample-rows N
      Include N representative rows from each detailed table in the lean data
      dictionary. Default: 3.

  --run-dir PATH
      Use a different CTSB v3.5-alpha run directory.

  --no-clipboard
      Create the bundle without copying it to the macOS clipboard.

  --help
      Show this help.

Default behaviour:
  Creates a lean dashboard-development bundle containing:

  - the dedicated dashboard prompt and controlling design README;
  - current methodology and alpha-status documentation;
  - the complete 100-audit comparison registry;
  - complete aggregate condition and shift statistics;
  - complete validation metrics;
  - sanitised run metadata;
  - data schemas, row counts, hashes, categories, and sample records;
  - alpha report and Azure diagnostic text with local paths sanitised;
  - public GitHub and GitHub Pages result locations;
  - local raw-vector file size, hash, array count, and dimensions;
  - and the complete research-first three-dimensional UMAP specification.

  The default bundle does not include raw-vector contents, caches, secrets,
  complete detailed result tables, backups, or unrelated archived materials.

Important:
  The selected CTSB v3.5-alpha result CSV files are already committed and can
  be read directly through GitHub Pages.

  The dashboard should fetch those result files from their current output
  paths rather than duplicate them unnecessarily.

  Raw vectors remain local. The dashboard implementation should use
  embeddings.npz locally to create one reproducible three-dimensional UMAP
  coordinate file. It should reuse those coordinates for three interactive
  views and publish only the coordinates and non-sensitive metadata.

  Do not calculate UMAP in the browser.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-code)
      WITH_CODE=1
      shift
      ;;
    --full-data)
      PROFILE="full-data"
      WITH_FULL_DATA=1
      shift
      ;;
    --sample-rows)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: --sample-rows requires an integer." >&2
        exit 1
      fi
      SAMPLE_ROWS="$2"
      shift 2
      ;;
    --run-dir)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: --run-dir requires a path." >&2
        exit 1
      fi
      RUN_DIR="$2"
      shift 2
      ;;
    --no-clipboard)
      COPY_TO_CLIPBOARD=0
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ ! "$SAMPLE_ROWS" =~ ^[0-9]+$ ]] || [[ "$SAMPLE_ROWS" -lt 1 ]]; then
  echo "ERROR: --sample-rows must be a positive integer." >&2
  exit 1
fi

if [[ ! -d "$PROJECT" ]]; then
  echo "ERROR: project folder not found:" >&2
  echo "  $PROJECT" >&2
  exit 1
fi

if [[ ! -d "$RUN_DIR" ]]; then
  echo "ERROR: alpha Azure run directory not found:" >&2
  echo "  $RUN_DIR" >&2
  exit 1
fi

if [[ -x "$PROJECT/.venv/bin/python" ]]; then
  PYTHON="$PROJECT/.venv/bin/python"
else
  PYTHON="python3"
fi

BENCHMARK_DIR="$PROJECT/data/benchmarks/v3_5_alpha/generated_100"
PROMPT_FILE="$PROJECT/docs/CTSB_V3_5_ALPHA_DASHBOARD_PROMPT.md"
DESIGN_FILE="$RUN_DIR/DASHBOARD_DESIGN_README.md"
EMBEDDINGS_FILE="$RUN_DIR/embeddings.npz"
EMBEDDING_INDEX_FILE="$RUN_DIR/embedding_index.csv"
RUN_NAME="$(basename "$RUN_DIR")"
RUN_REL="outputs/v3_5_alpha/runs/$RUN_NAME"
PUBLIC_RESULTS_BASE="https://yin-renlong.github.io/vector-space-theological-meaning/$RUN_REL"

REQUIRED_PROJECT_FILES=(
  "$PROMPT_FILE"
  "$DESIGN_FILE"
  "$PROJECT/README.md"
  "$PROJECT/VERSION"
  "$PROJECT/docs/CTSB_V3_5_ALPHA_PROTOCOL.md"
  "$PROJECT/data/benchmarks/v3_5_alpha/README.md"
  "$BENCHMARK_DIR/comparisons.csv"
  "$BENCHMARK_DIR/references.csv"
  "$BENCHMARK_DIR/queries.csv"
  "$BENCHMARK_DIR/validation.csv"
)

REQUIRED_RESULT_FILES=(
  "$RUN_DIR/embeddings.npz"
  "$RUN_DIR/embedding_index.csv"
  "$RUN_DIR/run_manifest.json"
  "$RUN_DIR/alpha_run_report.md"
  "$RUN_DIR/azure_diagnostic_report.txt"
  "$RUN_DIR/alpha_condition_statistics.csv"
  "$RUN_DIR/alpha_shift_statistics.csv"
  "$RUN_DIR/query_scores.csv"
  "$RUN_DIR/shifts.csv"
  "$RUN_DIR/validation_metrics.csv"
  "$RUN_DIR/validation_scores.csv"
  "$RUN_DIR/leave_one_reference_out_summary.csv"
  "$RUN_DIR/paraphrase_condition_sensitivity.csv"
  "$RUN_DIR/paraphrase_shift_sensitivity.csv"
)

for file in "${REQUIRED_PROJECT_FILES[@]}" "${REQUIRED_RESULT_FILES[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "ERROR: required dashboard-context file not found:" >&2
    echo "  $file" >&2
    exit 1
  fi
done

BUNDLE="$OUT_DIR/ctsb_v3_5_alpha_dashboard_context_${PROFILE}_$STAMP.txt"
LATEST="$OUT_DIR/ctsb_v3_5_alpha_dashboard_context_latest.txt"

mkdir -p "$OUT_DIR"
cd "$PROJECT"

export PROJECT RUN_DIR BENCHMARK_DIR SAMPLE_ROWS DESIGN_FILE EMBEDDINGS_FILE EMBEDDING_INDEX_FILE RUN_REL PUBLIC_RESULTS_BASE

emit_project_file() {
  local relative_path="$1"
  local absolute_path="$PROJECT/$relative_path"

  if [[ -f "$absolute_path" ]]; then
    echo "===== PROJECT FILE: $relative_path ====="
    cat "$absolute_path"
    echo ""
  else
    echo "===== MISSING OPTIONAL PROJECT FILE: $relative_path ====="
    echo ""
  fi
}

emit_result_file() {
  local filename="$1"
  local absolute_path="$RUN_DIR/$filename"

  if [[ -f "$absolute_path" ]]; then
    echo "===== RESULT FILE: $filename ====="
    cat "$absolute_path"
    echo ""
  else
    echo "===== MISSING OPTIONAL RESULT FILE: $filename ====="
    echo ""
  fi
}

{
  cat <<HEADER
CTSB v3.5-alpha — DASHBOARD DEVELOPMENT CONTEXT
================================================

NEW-THREAD REQUEST
Build a professional static GitHub Pages dashboard for:

  CTSB v3.5-alpha — Generated Exploratory 100-Concept Results

Read both controlling specifications before proposing changes:

1. docs/CTSB_V3_5_ALPHA_DASHBOARD_PROMPT.md
2. $RUN_REL/DASHBOARD_DESIGN_README.md

The design README controls the research-first visual architecture and the
three-dimensional UMAP plan.

CONTEXT PROFILE: $PROFILE
DETAILED SAMPLE ROWS PER TABLE: $SAMPLE_ROWS

CRITICAL STATUS
- The alpha is generated, unreviewed, exploratory, and non-evidential.
- The dashboard must not present alpha results as validated theology.
- Always distinguish S_C, S_R, CAS, Delta S_C, Delta S_R, and Delta CAS.
- Positive Delta CAS alone is not theological recovery.
- The perfect alpha development-validation score is not independent validation.
- Do not infer machine belief, consciousness, hostility, or deception.
- Do not expose secrets, endpoints, raw-vector contents, or caches.
- Do not publish local absolute paths in the dashboard.
- Do not replace the root v2 compatibility dashboard.
- Build the alpha dashboard at dashboards/v3_5_alpha/.
- The selected alpha result CSVs are committed and may be fetched directly.
- Do not duplicate complete result tables unnecessarily.
- Use local embeddings.npz only to generate one reproducible 3D UMAP.
- Publish only UMAP coordinates and non-sensitive preprocessing metadata.
- Reuse one UMAP fit for three interactive 3D views.
- Keep every UMAP explicitly exploratory.
- Numerical high-dimensional cosine analysis remains primary.

The lean bundle contains complete aggregate tables, data schemas, samples,
public paths, complete visual-design instructions, and safe local vector
metadata.

Complete detailed tables and raw vectors do not need to be inserted into the
AI prompt. The implementation script can read the complete local or committed
files directly.
HEADER

  echo ""
  echo "CURRENT GIT STATE"
  echo "================="
  echo "Repository: https://github.com/YIN-Renlong/vector-space-theological-meaning"
  echo "Branch: $(git branch --show-current 2>/dev/null || echo unknown)"
  echo "Commit: $(git rev-parse HEAD 2>/dev/null || echo unknown)"
  echo ""
  echo "Recent commits:"
  git log --oneline --max-count=8 2>/dev/null || true
  echo ""
  echo "Working tree:"
  git status --short 2>/dev/null || true

  echo ""
  echo "PUBLIC RESULT LOCATIONS"
  echo "======================="
  echo "Committed run path:"
  echo "  $RUN_REL"
  echo ""
  echo "GitHub result folder:"
  echo "  https://github.com/YIN-Renlong/vector-space-theological-meaning/tree/main/$RUN_REL"
  echo ""
  echo "GitHub Pages result-data base:"
  echo "  $PUBLIC_RESULTS_BASE"
  echo ""
  echo "Expected dashboard URL:"
  echo "  https://yin-renlong.github.io/vector-space-theological-meaning/dashboards/v3_5_alpha/"

  echo ""
  echo "DASHBOARD CONTROLLING DOCUMENTS"
  echo "==============================="
  emit_project_file "docs/CTSB_V3_5_ALPHA_DASHBOARD_PROMPT.md"
  emit_result_file "DASHBOARD_DESIGN_README.md"
  emit_project_file "README.md"
  emit_project_file "VERSION"
  emit_project_file "docs/CTSB_V3_5_ALPHA_PROTOCOL.md"
  emit_project_file "data/benchmarks/v3_5_alpha/README.md"

  if [[ -f "$PROJECT/docs/AI_HANDOFF_V3_5_BETA.md" ]]; then
    emit_project_file "docs/AI_HANDOFF_V3_5_BETA.md"
  fi

  echo ""
  echo "COMPLETE BENCHMARK COMPARISON REGISTRY"
  echo "======================================"
  emit_project_file "data/benchmarks/v3_5_alpha/generated_100/comparisons.csv"

  echo ""
  echo "COMPLETE AGGREGATE AZURE RESULTS"
  echo "================================"
  emit_result_file "alpha_condition_statistics.csv"
  emit_result_file "alpha_shift_statistics.csv"
  emit_result_file "validation_metrics.csv"

  echo ""
  echo "LOCAL RAW-VECTOR METADATA FOR 3D UMAP PREPROCESSING"
  echo "==================================================="

  "$PYTHON" <<'PY_VECTOR_METADATA'
from pathlib import Path
import hashlib
import json
import os

import numpy as np
import pandas as pd

embeddings_file = Path(os.environ["EMBEDDINGS_FILE"])
embedding_index_file = Path(os.environ["EMBEDDING_INDEX_FILE"])
run_rel = os.environ["RUN_REL"]

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

with np.load(embeddings_file, allow_pickle=False) as archive:
    array_names = list(archive.files)

index = pd.read_csv(embedding_index_file)

dimensions = (
    sorted(
        {
            int(value)
            for value in index["dimensions"].dropna().tolist()
        }
    )
    if "dimensions" in index.columns
    else []
)

metadata = {
    "raw_vectors_available_locally": True,
    "raw_vectors_included_in_context_bundle": False,
    "raw_vectors_intended_for_dashboard_runtime": False,
    "source_relative_path": f"{run_rel}/embeddings.npz",
    "filename": embeddings_file.name,
    "bytes": embeddings_file.stat().st_size,
    "sha256": sha256_file(embeddings_file),
    "npz_array_count": len(array_names),
    "embedding_index_rows": len(index),
    "reported_dimensions": dimensions,
    "required_umap_components": 3,
    "required_umap_views": 3,
    "required_umap_metric": "cosine",
    "recommended_n_neighbors": 30,
    "recommended_min_dist": 0.15,
    "required_random_seed": 42,
    "coordinate_publication_target": (
        f"{run_rel}/umap_3d_coordinates.csv"
    ),
    "optional_manifest_target": (
        f"{run_rel}/umap_3d_manifest.json"
    ),
    "instruction": (
        "Use embeddings.npz locally to compute one reproducible "
        "three-dimensional UMAP. Publish only embedding_id, umap_x, "
        "umap_y, umap_z, and non-sensitive preprocessing metadata. "
        "Reuse the same coordinates for all three interactive views."
    ),
}

print(json.dumps(metadata, ensure_ascii=False, indent=2))
PY_VECTOR_METADATA

  echo ""
  echo "SANITISED RUN METADATA"
  echo "======================"

  "$PYTHON" <<'PY'
from pathlib import Path
import json
import os

run_dir = Path(os.environ["RUN_DIR"])
manifest = json.loads(
    (run_dir / "run_manifest.json").read_text(encoding="utf-8")
)
model = manifest.get("model_metadata", {})

safe_manifest = {
    "methodology_version": manifest.get("methodology_version"),
    "implementation_stage": manifest.get("implementation_stage"),
    "evidential_status": manifest.get("evidential_status"),
    "generated_at_utc": manifest.get("generated_at_utc"),
    "backend": manifest.get("backend"),
    "git_commit": manifest.get("git_commit"),
    "run_purpose": manifest.get("run_purpose"),
    "model": {
        "provider": model.get("provider"),
        "requested_model": model.get("requested_model"),
        "response_model": model.get("response_model"),
        "api_version": model.get("api_version"),
        "embedding_dimensions": model.get("embedding_dimensions"),
        "new_embeddings": model.get("new_embeddings"),
        "cached_embeddings": model.get("cached_embeddings"),
    },
    "input_counts": manifest.get("input_counts"),
    "cas_definition": manifest.get("cas_definition"),
    "shift_definition": manifest.get("shift_definition"),
    "validation_status": manifest.get("validation_status"),
    "source_status": manifest.get("source_status"),
    "dashboard_status_at_run": manifest.get("dashboard_status"),
}

print(json.dumps(safe_manifest, ensure_ascii=False, indent=2))
PY

  echo ""
  echo "SANITISED ALPHA REPORTS"
  echo "======================="

  "$PYTHON" <<'PY'
from pathlib import Path
import os
import re

project = Path(os.environ["PROJECT"])
run_dir = Path(os.environ["RUN_DIR"])

for filename in (
    "alpha_run_report.md",
    "azure_diagnostic_report.txt",
):
    path = run_dir / filename
    print(f"===== SANITISED REPORT: {filename} =====")

    text = path.read_text(encoding="utf-8", errors="replace")
    text = text.replace(str(project), "$PROJECT")
    text = re.sub(
        r"/Users/[^/\s]+",
        "$HOME",
        text,
    )

    print(text.rstrip())
    print("")
PY

  echo ""
  echo "DETAILED DATA DICTIONARY, HASHES, CATEGORIES, AND SAMPLES"
  echo "========================================================="

  "$PYTHON" <<'PY'
from pathlib import Path
import hashlib
import json
import os

import pandas as pd

project = Path(os.environ["PROJECT"])
run_dir = Path(os.environ["RUN_DIR"])
benchmark_dir = Path(os.environ["BENCHMARK_DIR"])
sample_rows = int(os.environ["SAMPLE_ROWS"])

files = [
    (
        "benchmark/references.csv",
        benchmark_dir / "references.csv",
    ),
    (
        "benchmark/queries.csv",
        benchmark_dir / "queries.csv",
    ),
    (
        "benchmark/validation.csv",
        benchmark_dir / "validation.csv",
    ),
    (
        "results/embedding_index.csv",
        run_dir / "embedding_index.csv",
    ),
    (
        "results/query_scores.csv",
        run_dir / "query_scores.csv",
    ),
    (
        "results/shifts.csv",
        run_dir / "shifts.csv",
    ),
    (
        "results/condition_summary.csv",
        run_dir / "condition_summary.csv",
    ),
    (
        "results/validation_scores.csv",
        run_dir / "validation_scores.csv",
    ),
    (
        "results/leave_one_reference_out_summary.csv",
        run_dir / "leave_one_reference_out_summary.csv",
    ),
    (
        "results/paraphrase_condition_sensitivity.csv",
        run_dir / "paraphrase_condition_sensitivity.csv",
    ),
    (
        "results/paraphrase_shift_sensitivity.csv",
        run_dir / "paraphrase_shift_sensitivity.csv",
    ),
    (
        "results/similarities.csv",
        run_dir / "similarities.csv",
    ),
]

category_columns = {
    "audit_id",
    "primary_locus",
    "comparison_register",
    "relationship_type",
    "condition",
    "context",
    "contrast_type",
    "reference_group",
    "validation_stage",
    "target_class",
    "top_reference_group",
    "life_death_module",
    "roles",
}

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

for display_name, path in files:
    print("=" * 78)
    print(f"TABLE: {display_name}")
    print("=" * 78)

    if not path.exists():
        print("STATUS: missing optional file")
        print("")
        continue

    frame = pd.read_csv(path)

    print(f"Rows: {len(frame)}")
    print(f"Columns: {len(frame.columns)}")
    print(f"Bytes: {path.stat().st_size}")
    print(f"SHA-256: {sha256_file(path)}")
    print("")
    print("Column schema:")

    for column in frame.columns:
        null_count = int(frame[column].isna().sum())
        print(
            f"  - {column}: dtype={frame[column].dtype}; "
            f"nulls={null_count}"
        )

    available_categories = [
        column
        for column in frame.columns
        if column in category_columns
    ]

    if available_categories:
        print("")
        print("Selected categorical values:")

        for column in available_categories:
            values = sorted(
                {
                    str(value)
                    for value in frame[column].dropna().unique()
                }
            )

            if len(values) <= 30:
                print(
                    f"  - {column}: "
                    + json.dumps(values, ensure_ascii=False)
                )
            else:
                print(
                    f"  - {column}: {len(values)} unique values; "
                    + json.dumps(values[:10], ensure_ascii=False)
                    + " ..."
                )

    print("")
    print(f"First {min(sample_rows, len(frame))} representative rows:")
    print(
        frame.head(sample_rows).to_json(
            orient="records",
            indent=2,
            force_ascii=False,
        )
    )
    print("")
PY

  if [[ "$WITH_CODE" -eq 1 ]]; then
    echo ""
    echo "OPTIONAL IMPLEMENTATION SOURCE"
    echo "=============================="
    emit_project_file "scripts/ctsb_v3_5_alpha.py"
    emit_project_file "scripts/ctsb_v3_4_prototype.py"
    emit_project_file "tests/test_ctsb_v3_5_alpha.py"
    emit_project_file "tests/test_ctsb_v3_4_prototype.py"
  fi

  if [[ "$WITH_FULL_DATA" -eq 1 ]]; then
    echo ""
    echo "COMPLETE SELECTED TABULAR DATA"
    echo "=============================="
    echo ""
    echo "WARNING: This section may be very large."
    echo ""

    FULL_PROJECT_FILES=(
      "data/benchmarks/v3_5_alpha/generated_100/references.csv"
      "data/benchmarks/v3_5_alpha/generated_100/queries.csv"
      "data/benchmarks/v3_5_alpha/generated_100/validation.csv"
    )

    for relative_path in "${FULL_PROJECT_FILES[@]}"; do
      emit_project_file "$relative_path"
    done

    FULL_RESULT_FILES=(
      "embedding_index.csv"
      "query_scores.csv"
      "shifts.csv"
      "condition_summary.csv"
      "validation_scores.csv"
      "leave_one_reference_out_summary.csv"
      "paraphrase_condition_sensitivity.csv"
      "paraphrase_shift_sensitivity.csv"
      "similarities.csv"
    )

    for filename in "${FULL_RESULT_FILES[@]}"; do
      emit_result_file "$filename"
    done
  fi

  echo ""
  echo "PUBLICATION AND EXCLUSION POLICY"
  echo "================================"
  echo "Already committed and directly readable through GitHub Pages:"
  echo "- selected alpha aggregate, query, shift, validation, and robustness tables"
  echo "- embedding_index.csv"
  echo "- DASHBOARD_DESIGN_README.md"
  echo ""
  echo "Available locally for preprocessing but not inserted into this bundle:"
  echo "- embeddings.npz"
  echo ""
  echo "Derived files to create and publish:"
  echo "- umap_3d_coordinates.csv"
  echo "- optional umap_3d_manifest.json"
  echo ""
  echo "Explicitly excluded:"
  echo "- raw contents of embeddings.npz"
  echo "- embedding_cache.json"
  echo "- .env"
  echo "- API credentials and endpoints"
  echo "- local backups"
  echo "- unrelated output runs"
  echo "- archived v2 data and dashboards"

  echo ""
  echo "END OF CTSB v3.5-alpha DASHBOARD CONTEXT"
} > "$BUNDLE"

cp -f "$BUNDLE" "$LATEST"

BYTES="$(wc -c < "$BUNDLE" | tr -d ' ')"
LINES="$(wc -l < "$BUNDLE" | tr -d ' ')"
APPROX_TOKENS="$((BYTES / 4))"

if grep -q "===== RESULT FILE: embeddings.npz =====" "$BUNDLE"; then
  echo "ERROR: raw vectors were included unexpectedly." >&2
  exit 1
fi

if grep -q "AZURE_OPENAI_API_KEY=" "$BUNDLE"; then
  echo "ERROR: an Azure API-key field was included unexpectedly." >&2
  exit 1
fi

if grep -Eq \
  '===== PROJECT FILE: \.env =====|===== RESULT FILE: embedding_cache\.json =====' \
  "$BUNDLE"
then
  echo "ERROR: a private file was included unexpectedly." >&2
  exit 1
fi

if [[ "$COPY_TO_CLIPBOARD" -eq 1 ]] && command -v pbcopy >/dev/null 2>&1; then
  pbcopy < "$BUNDLE"
  echo "Dashboard context copied to the macOS clipboard."
fi

echo ""
echo "Dashboard context created:"
echo "  $BUNDLE"
echo ""
echo "Latest dashboard context:"
echo "  $LATEST"
echo ""
echo "Profile:"
echo "  $PROFILE"
echo ""
echo "Source run:"
echo "  ${RUN_DIR#"$PROJECT/"}"
echo ""
echo "Committed public result base:"
echo "  $PUBLIC_RESULTS_BASE"
echo ""
echo "Controlling dashboard design:"
echo "  ${DESIGN_FILE#"$PROJECT/"}"
echo ""
echo "3D UMAP preprocessing:"
echo "  embeddings.npz is available locally but not copied into the context."
echo "  Generate one umap_3d_coordinates.csv and reuse it for all three views."
echo ""
echo "Size:"
echo "  $BYTES bytes"
echo "  $LINES lines"
echo "  approximately $APPROX_TOKENS tokens"
echo ""
echo "Included active implementation code:"
if [[ "$WITH_CODE" -eq 1 ]]; then
  echo "  yes"
else
  echo "  no"
fi
echo ""
echo "Included complete detailed tabular data:"
if [[ "$WITH_FULL_DATA" -eq 1 ]]; then
  echo "  yes — potentially very large"
else
  echo "  no — schemas, hashes, categories, and samples only"
fi
echo ""
echo "Raw vector contents, caches, and secrets included:"
echo "  no"
echo ""
echo "Local raw-vector metadata included:"
echo "  yes — filename, size, hash, array count, and dimensions only"
echo ""
echo "Three-dimensional dashboard design included:"
echo "  yes"
echo ""
echo "New-thread instruction:"
echo "  Paste the latest dashboard context into a new AI thread."
echo "  Ask the AI to provide architecture and data mapping before code."
