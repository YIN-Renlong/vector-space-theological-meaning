#!/usr/bin/env bash
set -euo pipefail

PROJECT="/Users/Renlong/Projects/GitHub/YIN-Renlong/vector-space-theological-meaning"
OUT_DIR="$PROJECT/ai_context"
STAMP="$(date +%Y%m%d-%H%M%S)"
BUNDLE="$OUT_DIR/ctsb_v3_4_ai_context_$STAMP.txt"
LATEST="$OUT_DIR/ctsb_v3_4_ai_context_latest.txt"
V2_ARCHIVE="$PROJECT/archive/ctsb_100_v2_context_draft"

mkdir -p "$OUT_DIR"
cd "$PROJECT"

{
  cat <<'HEADER'
CTSB v3.4 — NEW AI THREAD CONTEXT BUNDLE
=========================================
CONTINUATION REQUEST
You are continuing the project “Vector Space and Theological Meaning”.
Read the active README and AI handoff before proposing changes.
The active methodology is CTSB v3.4.
The archived v2 Python files included at the end are historical implementation references only. Do not copy the v2 methodology unchanged.
HEADER

  echo ""
  echo "ACTIVE PROJECT STRUCTURE"
  echo "========================"
  find . -maxdepth 5 ! -path './.git*' ! -path './archive*' ! -path './_patch_backups*' ! -path './ai_context*' ! -path '*__pycache__*' ! -name '*.pyc' ! -name 'azure_embeddings_cache.json' -print | LC_ALL=C sort

  echo ""
  echo "ACTIVE V3.4 FILES"
  echo "================="
  # SINGLE LINE TO PREVENT TERMINAL COPY-PASTE BUGS:
  files-to-prompt "$PROJECT" --ignore "*.html" --ignore "*.png" --ignore "*.jpg" --ignore "*.pdf" --ignore "azure_embeddings_cache.json" --ignore "archive/**" --ignore "_patch_backups/**" --ignore "ai_context/**" --ignore ".git/**" --ignore ".env" --ignore ".venv/**" --ignore "__pycache__" --ignore "*.pyc" --ignore ".DS_Store" --ignore "LICENSE"

  echo ""
  echo "SELECTED LEGACY V2 FILES (Reference Only)"
  echo "========================================="
  LEGACY_FILES=("$V2_ARCHIVE/scripts/audit_azure_embeddings.py" "$V2_ARCHIVE/scripts/audit_life_death_embeddings.py" "$V2_ARCHIVE/docs/statistical_analysis_plan.md")
  for file in "${LEGACY_FILES[@]}"; do
    if [ -f "$file" ]; then
      echo "===== LEGACY FILE: ${file#"$PROJECT/"} ====="
      cat "$file"
      echo ""
    fi
  done

  echo "END OF CONTEXT BUNDLE"
} > "$BUNDLE"

cp -f "$BUNDLE" "$LATEST"
if command -v pbcopy >/dev/null 2>&1; then
  pbcopy < "$BUNDLE"
  echo "Bundle copied to macOS clipboard."
fi
echo "Context bundle created at: $LATEST"
