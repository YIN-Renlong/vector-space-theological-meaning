#!/usr/bin/env bash
set -euo pipefail

PROJECT="/Users/Renlong/Projects/GitHub/YIN-Renlong/vector-space-theological-meaning"
OUT_DIR="$PROJECT/ai_context"
STAMP="$(date +%Y%m%d-%H%M%S)"
PROFILE="lean"
WITH_ACTIVE_CODE=0
WITH_ALPHA_DATA=0
WITH_LEGACY_V2=0
COPY_TO_CLIPBOARD=1
V2_ARCHIVE="$PROJECT/archive/ctsb_100_v2_context_draft"

usage() {
  cat <<'USAGE'
Usage:
  ./tools/build_ai_context.sh [options]

Options:
  --full
      Include the complete development log, historical alpha handoff,
      active source code and tests, v3.4 engine and tests, context-builder
      source, and generated alpha CSVs.

  --with-code
      Include the active v3.5-alpha generator and tests. These are omitted
      from the default lean beta-planning bundle to reduce bundle size.

  --with-alpha-data
      Include all four generated CTSB v3.5-alpha CSV tables without enabling
      the complete full profile.

  --with-legacy-v2
      Include selected archived v2 implementation files. This remains off by
      default because v2 is historical only.

  --no-clipboard
      Create the bundle without copying it to the macOS clipboard.

  --help
      Show this help.

Default behaviour:
  Creates a lean CTSB v3.5-beta continuation bundle containing the current
  README, version, active beta handoff and plan, alpha protocol and benchmark
  status, and requirements.

  The lean profile omits the full development log, active source code and
  tests, generated alpha CSV tables, v3.4 engine source, local outputs, raw
  vectors, caches, dashboards, backups, archived handoffs, AI-context history,
  and v2 materials.

  Use --with-code when a new thread must inspect or modify the implementation.
  Important alpha results and current restrictions are summarised in the beta
  handoff, so local generated runs are never required in the standard bundle.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --full)
      PROFILE="full"
      WITH_ACTIVE_CODE=1
      WITH_ALPHA_DATA=1
      shift
      ;;
    --with-code)
      WITH_ACTIVE_CODE=1
      shift
      ;;
    --with-alpha-data)
      WITH_ALPHA_DATA=1
      shift
      ;;
    --with-legacy-v2)
      WITH_LEGACY_V2=1
      shift
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

if [[ ! -d "$PROJECT" ]]; then
  echo "ERROR: project folder not found:" >&2
  echo "  $PROJECT" >&2
  exit 1
fi

BUNDLE="$OUT_DIR/ctsb_v3_5_beta_ai_context_${PROFILE}_$STAMP.txt"
LATEST="$OUT_DIR/ctsb_v3_5_beta_ai_context_latest.txt"
GENERIC_LATEST="$OUT_DIR/ctsb_ai_context_latest.txt"

mkdir -p "$OUT_DIR"
cd "$PROJECT"

emit_file() {
  local relative_path="$1"
  local absolute_path="$PROJECT/$relative_path"

  if [[ -f "$absolute_path" ]]; then
    echo "===== ACTIVE FILE: $relative_path ====="
    cat "$absolute_path"
    echo ""
  else
    echo "===== MISSING OPTIONAL FILE: $relative_path ====="
    echo ""
  fi
}

ACTIVE_FILES=(
  "README.md"
  "VERSION"
  "docs/AI_HANDOFF_V3_5_BETA.md"
  "docs/CTSB_V3_5_BETA_PLAN.md"
  "docs/CTSB_V3_5_ALPHA_PROTOCOL.md"
  "data/benchmarks/v3_5_alpha/README.md"
  "requirements.txt"
)

if [[ -f "$PROJECT/.env.example" ]]; then
  ACTIVE_FILES+=(".env.example")
fi

if [[ "$WITH_ACTIVE_CODE" -eq 1 ]]; then
  ACTIVE_FILES+=(
    "scripts/ctsb_v3_5_alpha.py"
    "tests/test_ctsb_v3_5_alpha.py"
  )
fi

if [[ "$PROFILE" == "full" ]]; then
  ACTIVE_FILES+=(
    "DEVELOPMENT_LOG.md"
    "docs/AI_HANDOFF_V3_5_ALPHA.md"
    "docs/AI_HANDOFF_V3_4.md"
    "data/benchmarks/v3_4/README.md"
    "scripts/ctsb_v3_4_prototype.py"
    "tests/test_ctsb_v3_4_prototype.py"
    "tools/build_ai_context.sh"
  )
fi

if [[ "$WITH_ALPHA_DATA" -eq 1 ]]; then
  ACTIVE_FILES+=(
    "data/benchmarks/v3_5_alpha/generated_100/comparisons.csv"
    "data/benchmarks/v3_5_alpha/generated_100/references.csv"
    "data/benchmarks/v3_5_alpha/generated_100/queries.csv"
    "data/benchmarks/v3_5_alpha/generated_100/validation.csv"
  )
fi

{
  cat <<HEADER
CTSB v3.5-beta — NEW AI THREAD CONTEXT BUNDLE
==============================================

CONTINUATION REQUEST
You are continuing the project “Vector Space and Theological Meaning”.

Read README.md and docs/AI_HANDOFF_V3_5_BETA.md before proposing changes.

CTSB v3.5-alpha is complete as a generated, non-evidential 100-concept
development experiment.

The next planned phase is CTSB v3.5-beta.

The immediate task is a focused beta construction pilot that reduces template
and label leakage, separates reference/query/validation authoring, and
operationalises theological framing–content divergence before another
100-concept or Azure run.

BUNDLE PROFILE: $PROFILE

IMPORTANT RESTRICTIONS
- Alpha references, validation passages, and results are generated and
  non-evidential.
- Do not present candidate sources as verified support for generated wording.
- Do not treat perfect alpha development validation as independent validation.
- Do not restore the broad v2 secular/common-language category.
- Do not interpret positive CAS alone as theological recovery.
- Do not infer machine consciousness, subconscious bias, belief, hostility,
  or intentional deception.
- Do not immediately regenerate all 100 concepts or rerun Azure.
- Do not begin dashboard work before the beta instrument is stable.
- Do not expose or request local secrets.
- Raw vectors, caches, generated runs, dashboards, backups, AI-context history,
  and handoff archives are intentionally omitted from the standard bundle.

The lean profile omits the full DEVELOPMENT_LOG.md, active implementation
source and tests, and generated alpha CSVs because the active beta handoff
contains the current state, decisions, results, limitations, restrictions,
and immediate next action.

Use --full only when detailed chronology, v3.4 engine internals, and all alpha
source tables are genuinely needed.
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
  echo "CURATED ACTIVE PROJECT STRUCTURE"
  echo "================================"
  find . -maxdepth 5 \
    ! -path './.git*' \
    ! -path './.venv*' \
    ! -path './archive*' \
    ! -path './_patch_backups*' \
    ! -path './ai_context*' \
    ! -path './outputs*' \
    ! -path './docs/handoff_archive*' \
    ! -path '*/__pycache__*' \
    ! -name '*.pyc' \
    ! -name '.DS_Store' \
    ! -name '.env' \
    ! -name '*.html' \
    ! -name '*.png' \
    ! -name '*.jpg' \
    ! -name '*.pdf' \
    -print |
    LC_ALL=C sort

  echo ""
  echo "ACTIVE CTSB v3.5-beta CONTINUATION FILES"
  echo "========================================"
  for relative_path in "${ACTIVE_FILES[@]}"; do
    emit_file "$relative_path"
  done

  if [[ "$WITH_LEGACY_V2" -eq 1 ]]; then
    echo ""
    echo "SELECTED LEGACY V2 FILES — HISTORICAL REFERENCE ONLY"
    echo "====================================================="

    LEGACY_FILES=(
      "$V2_ARCHIVE/docs/statistical_analysis_plan.md"
      "$V2_ARCHIVE/scripts/audit_azure_embeddings.py"
      "$V2_ARCHIVE/scripts/audit_life_death_embeddings.py"
    )

    for file in "${LEGACY_FILES[@]}"; do
      if [[ -f "$file" ]]; then
        echo "===== LEGACY FILE: ${file#"$PROJECT/"} ====="
        cat "$file"
        echo ""
      fi
    done
  fi

  echo "END OF CONTEXT BUNDLE"
} > "$BUNDLE"

cp -f "$BUNDLE" "$LATEST"
cp -f "$BUNDLE" "$GENERIC_LATEST"

BYTES="$(wc -c < "$BUNDLE" | tr -d ' ')"
LINES="$(wc -l < "$BUNDLE" | tr -d ' ')"
APPROX_TOKENS="$((BYTES / 4))"

if [[ "$COPY_TO_CLIPBOARD" -eq 1 ]] && command -v pbcopy >/dev/null 2>&1; then
  pbcopy < "$BUNDLE"
  echo "Bundle copied to macOS clipboard."
fi

echo ""
echo "Context bundle created:"
echo "  $BUNDLE"
echo ""
echo "Latest beta bundle:"
echo "  $LATEST"
echo ""
echo "Generic latest bundle:"
echo "  $GENERIC_LATEST"
echo ""
echo "Profile:"
echo "  $PROFILE"
echo ""
echo "Size:"
echo "  $BYTES bytes"
echo "  $LINES lines"
echo "  approximately $APPROX_TOKENS tokens using a rough bytes/4 estimate"
echo ""
echo "Included active source code and tests:"
if [[ "$WITH_ACTIVE_CODE" -eq 1 ]]; then
  echo "  yes"
else
  echo "  no"
fi
echo ""
echo "Included generated alpha CSV data:"
if [[ "$WITH_ALPHA_DATA" -eq 1 ]]; then
  echo "  yes"
else
  echo "  no"
fi
echo ""
echo "Included legacy v2 files:"
if [[ "$WITH_LEGACY_V2" -eq 1 ]]; then
  echo "  yes — historical reference only"
else
  echo "  no"
fi
