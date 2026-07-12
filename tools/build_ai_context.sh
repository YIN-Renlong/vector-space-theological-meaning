#!/usr/bin/env bash
set -euo pipefail

PROJECT="/Users/Renlong/Projects/GitHub/YIN-Renlong/vector-space-theological-meaning"
OUT_DIR="$PROJECT/ai_context"
STAMP="$(date +%Y%m%d-%H%M%S)"
PROFILE="lean"
WITH_LEGACY_V2=0
COPY_TO_CLIPBOARD=1
V2_ARCHIVE="$PROJECT/archive/ctsb_100_v2_context_draft"

usage() {
  cat <<'USAGE'
Usage:
  ./tools/build_ai_context.sh [options]

Options:
  --full
      Include the complete root DEVELOPMENT_LOG.md and context-builder source.

  --with-legacy-v2
      Include selected archived v2 implementation files. This is off by
      default because active v3.4 code now exists.

  --no-clipboard
      Create the bundle without copying it to the macOS clipboard.

  --help
      Show this help.

Default behaviour:
  Creates a lean active-v3.4 bundle containing the methodology, current
  handoff, prototype benchmark inputs, active Python code, and tests.
  It excludes secrets, virtual environments, raw vectors, caches, generated
  outputs, dashboards, backups, AI-context history, handoff archives, and v2.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --full)
      PROFILE="full"
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

BUNDLE="$OUT_DIR/ctsb_v3_4_ai_context_${PROFILE}_$STAMP.txt"
LATEST="$OUT_DIR/ctsb_v3_4_ai_context_latest.txt"

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
  "docs/AI_HANDOFF_V3_4.md"
  "data/benchmarks/v3_4/README.md"
  "data/benchmarks/v3_4/prototype/comparisons.csv"
  "data/benchmarks/v3_4/prototype/references.csv"
  "data/benchmarks/v3_4/prototype/queries.csv"
  "data/benchmarks/v3_4/prototype/validation.csv"
  "scripts/ctsb_v3_4_prototype.py"
  "tests/test_ctsb_v3_4_prototype.py"
  "requirements.txt"
)

if [[ -f "$PROJECT/.env.example" ]]; then
  ACTIVE_FILES+=(".env.example")
fi

if [[ "$PROFILE" == "full" ]]; then
  ACTIVE_FILES+=(
    "DEVELOPMENT_LOG.md"
    "tools/build_ai_context.sh"
  )
fi

{
  cat <<HEADER
CTSB v3.4 — NEW AI THREAD CONTEXT BUNDLE
=========================================

CONTINUATION REQUEST
You are continuing the project “Vector Space and Theological Meaning”.

Read README.md and docs/AI_HANDOFF_V3_4.md before proposing changes.

The active methodology is CTSB v3.4.
Step 1 is complete.
The immediate task is the source-grounded five-audit pilot described in the
active handoff.

BUNDLE PROFILE: $PROFILE

IMPORTANT RESTRICTIONS
- Prototype references and outputs are synthetic and non-evidential.
- Archived v2 materials are historical references only.
- Do not restore the broad v2 secular/common-language category.
- Do not begin dashboard work before the numerical instrument is stable.
- Do not expose or request local secrets.
- Raw vectors, caches, generated runs, dashboards, backups, and handoff
  archives are intentionally omitted from the standard bundle.

The lean profile omits the full DEVELOPMENT_LOG.md because the active handoff
contains the current state, decisions, results, restrictions, and next action.
Use --full only when detailed chronological history is needed.
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
  echo "ACTIVE CTSB v3.4 FILES"
  echo "======================"
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
echo "Latest bundle:"
echo "  $LATEST"
echo ""
echo "Profile:"
echo "  $PROFILE"
echo ""
echo "Size:"
echo "  $BYTES bytes"
echo "  $LINES lines"
echo "  approximately $APPROX_TOKENS tokens using a rough bytes/4 estimate"
echo ""
echo "Included legacy v2 files:"
if [[ "$WITH_LEGACY_V2" -eq 1 ]]; then
  echo "  yes — historical reference only"
else
  echo "  no"
fi
