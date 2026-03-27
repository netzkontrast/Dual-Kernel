#!/bin/bash
set -euo pipefail

# ETL Pipeline Batch Runner for Kohärenz Protokoll
# Automates the full extraction, validation, and analysis pipeline
# Usage: ./tools/run_pipeline.sh [--help|--batch|--validate|--analyze]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Ensure virtual environment is activated
if [ -z "${VIRTUAL_ENV:-}" ]; then
  if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
  else
    echo -e "${RED}Error: Virtual environment not found. Run ./setup.sh first.${NC}"
    exit 1
  fi
fi

function print_phase() {
  echo -e "\n${GREEN}=== $1 ===${NC}\n"
}

function print_error() {
  echo -e "${RED}Error: $1${NC}"
  exit 1
}

function run_extraction() {
  print_phase "PHASE 1: EXTRACTION"

  echo "Scanning all markdown files in Markdown-docs/..."
  for file in Markdown-docs/*.md; do
    echo "  Scanning: $(basename "$file")"
    python tools/source_scanner.py --file "$file" 2>&1 | grep -E "(entities|mentions)" || true
  done

  echo "Finding cross-references and conflicts..."
  python tools/xref_finder.py || print_error "xref_finder.py failed"

  echo "Run 'python tools/conflict_diff.py' to review conflicts interactively."
  echo "Then run 'python tools/entity_generator.py' to generate entity files."
}

function run_validation() {
  print_phase "PHASE 2: VALIDATION"

  local failed=0

  echo "Validating YAML frontmatter..."
  if python tools/frontmatter_validator.py knowledge-graph/ 2>&1 | tail -3; then
    echo -e "${GREEN}✓ YAML validation passed${NC}"
  else
    echo -e "${RED}✗ YAML validation failed${NC}"
    failed=1
  fi

  echo ""
  echo "Checking wikilink integrity..."
  if python tools/wikilink_checker.py knowledge-graph/ 2>&1 | tail -3; then
    echo -e "${GREEN}✓ Wikilink check passed${NC}"
  else
    echo -e "${RED}✗ Wikilink check failed${NC}"
    failed=1
  fi

  echo ""
  echo "Checking narrative consistency..."
  if python tools/consistency_checker.py knowledge-graph/ 2>&1 | tail -3; then
    echo -e "${GREEN}✓ Consistency check passed${NC}"
  else
    echo -e "${RED}✗ Consistency check failed${NC}"
    failed=1
  fi

  if [ $failed -eq 1 ]; then
    print_error "Validation failed. Fix issues above before proceeding to Phase 3."
  fi

  echo -e "\n${GREEN}✓ All validators passed${NC}"
}

function run_analysis() {
  print_phase "PHASE 3: ANALYSIS & REPORTING"

  echo "Generating statistics..."
  python tools/entity_stats.py || print_error "entity_stats.py failed"

  echo ""
  echo "Generating relationship graph..."
  python tools/relationship_graph.py || print_error "relationship_graph.py failed"

  echo ""
  echo "Mapping entities to chapters..."
  python tools/chapter_mapper.py || print_error "chapter_mapper.py failed"

  echo ""
  echo "Building glossary..."
  python tools/glossary_generator.py --discover || print_error "glossary_generator.py failed"

  echo ""
  echo "Resolving canon status..."
  python tools/canon_resolver.py || print_error "canon_resolver.py failed"

  echo -e "\n${GREEN}✓ Analysis complete. Reports in knowledge-graph/_index/${NC}"
}

function run_full() {
  run_extraction

  echo ""
  echo -e "${YELLOW}MANUAL STEP REQUIRED:${NC}"
  echo "Run 'python tools/conflict_diff.py' to interactively review and resolve conflicts."
  echo "Then run 'python tools/entity_generator.py' to generate entity markdown files."
  echo "Finally, run this script again with '--validate' to check the generated entities."
}

function usage() {
  cat << EOF
Usage: ./tools/run_pipeline.sh [COMMAND]

Commands:
  --extract      Run Phase 1 (extract entities from Markdown-docs/)
  --validate     Run Phase 2 (validate YAML schema, wikilinks, consistency)
  --analyze      Run Phase 3 (generate reports and visualizations)
  --batch        Run full pipeline (extract → validation → analysis)
  --help         Show this help message

Default (no args): Run Phase 1 with instructions for manual conflict resolution

Examples:
  ./tools/run_pipeline.sh                  # Extract phase with manual conflict review
  ./tools/run_pipeline.sh --validate       # Validate generated entities
  ./tools/run_pipeline.sh --batch          # Full automated pipeline
EOF
}

# Main
case "${1:-}" in
  --extract)
    run_extraction
    ;;
  --validate)
    run_validation
    ;;
  --analyze)
    run_analysis
    ;;
  --batch)
    run_extraction
    run_validation
    run_analysis
    echo -e "\n${GREEN}✓ Full pipeline complete${NC}"
    ;;
  --help|-h)
    usage
    ;;
  *)
    if [ -z "${1:-}" ]; then
      run_full
    else
      echo "Unknown command: $1"
      usage
      exit 1
    fi
    ;;
esac
