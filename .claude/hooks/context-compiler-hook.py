#!/usr/bin/env python3
"""SessionStart hook: inject compiled context from context-compiler skill.

Reads the K1 (Semantic/Kohärenz) memory from the MIF memory file and
injects it as additionalContext at session start. This bootstraps every
new session with the last known stable context-synthesis.

Falls back silently if memory files don't exist yet (first run).
Never blocks the user — all errors are swallowed.
"""
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent.parent
MEMORY_MD = REPO_ROOT / ".claude" / "skills" / "context-compiler" / ".memory.md"
COMPILED_CONTEXT = REPO_ROOT / ".claude" / "compiled-context.md"

# Skills that form the compilation target
SKILL_MANIFEST = [
    ("context-fundamentals",          "Attention-Mechanik, Signal-Density-Test"),
    ("context-degradation",           "Lost-in-Middle, 4-Bucket-Mitigation"),
    ("context-compression",           "Tokens-per-Task, Artifact-Trail"),
    ("context-optimization",          "Compaction-Trigger, Observation-Masking"),
    ("context-engineering-collection","Meta-Hub: alle 11 Context-Skills"),
    ("multi-agent-patterns",          "Supervisor/Peer/Hierarchisch, Context-Isolation"),
    ("memory-systems",                "Scratchpad bis Temporal-KG"),
    ("tool-design",                   "Consolidation-Prinzip, Error-Context"),
    ("evaluation",                    "LLM-as-Judge, Multi-Dim-Rubrik"),
    ("filesystem-context",            "Plan-Persistence, Subagent-Komm."),
    ("hosted-agents",                 "Background-Agent-Infrastruktur"),
    ("prompt-architect",              "27 Frameworks — adversariale Quelle für K0"),
]


def parse_k1_from_memory(text: str) -> dict:
    """Extract the latest K1/Semantic section from .memory.md."""
    result = {
        "synthesis": None,
        "next_seed": None,
        "stability_score": None,
        "iteration": 0,
        "convergence": None,
    }

    # Find the latest iteration index from frontmatter
    iter_match = re.search(r"^iteration:\s*(\d+)", text, re.MULTILINE)
    if iter_match:
        result["iteration"] = int(iter_match.group(1))

    # Find the last Semantic Memory block
    semantic_blocks = list(re.finditer(
        r"## Semantic Memories.*?(?=^## |\Z)",
        text, re.MULTILINE | re.DOTALL
    ))
    if not semantic_blocks:
        return result

    last_block = semantic_blocks[-1].group(0)

    for field, pattern in [
        ("synthesis",       r"\*\*synthesis\*\*:\s*(.+)"),
        ("next_seed",       r"\*\*next_seed\*\*:\s*(.+)"),
        ("convergence",     r"\*\*convergence\*\*:\s*(.+)"),
        ("stability_score", r"\*\*stability_score\*\*:\s*([\d.]+)"),
    ]:
        m = re.search(pattern, last_block)
        if m:
            result[field] = m.group(1).strip()

    return result


def parse_aegis_rules(text: str) -> list[str]:
    """Extract active rules from the latest AEGIS/Procedural section."""
    rules = []
    proc_blocks = list(re.finditer(
        r"## Procedural Memories.*?(?=^## |\Z)",
        text, re.MULTILINE | re.DOTALL
    ))
    if not proc_blocks:
        return rules

    last_block = proc_blocks[-1].group(0)
    for m in re.finditer(r"\*\*rule\*\*:\s*(.+)", last_block):
        rules.append(m.group(1).strip())

    return rules


def build_context(k1: dict, rules: list[str], has_compiled: bool) -> str:
    """Build the additionalContext string for Claude."""
    lines = [
        "[Context-Compiler] Autopoietischer Loop aktiv",
        f"Iteration: {k1['iteration']} | "
        f"Stabilität: {k1['stability_score'] or '0.0'}",
        "",
    ]

    if k1["synthesis"]:
        lines += ["K1-Synthese (letzter Stand):", f"  {k1['synthesis']}", ""]

    if k1["next_seed"]:
        lines += ["Nächster Seed:", f"  {k1['next_seed']}", ""]

    if rules:
        lines += ["Aktive AEGIS-Regeln:"]
        for r in rules[:4]:  # max 4 rules in context
            lines.append(f"  • {r}")
        lines.append("")

    lines += [
        "Context-Skills (Compile-Rohstoff):",
    ]
    for name, desc in SKILL_MANIFEST[:6]:  # top 6 for brevity
        lines.append(f"  • {name}: {desc}")
    lines.append("  … (+ 6 weitere, siehe context-compiler/SKILL.md)")

    if has_compiled:
        lines += ["", "compiled-context.md verfügbar — letzte Kompilierung aktiv."]
    else:
        lines += ["", "Kein compiled-context.md — führe /context-compiler aus für ersten Compile."]

    return "\n".join(lines)


def main() -> None:
    try:
        # Read stdin (Claude Code hook event — ignored, we use file state)
        sys.stdin.read()

        if not MEMORY_MD.exists():
            sys.exit(0)

        memory_text = MEMORY_MD.read_text(encoding="utf-8")
        k1 = parse_k1_from_memory(memory_text)
        rules = parse_aegis_rules(memory_text)
        has_compiled = COMPILED_CONTEXT.exists()

        # Only inject if there's something meaningful (iteration > 0 or compiled exists)
        if k1["iteration"] == 0 and not has_compiled:
            # Seed state: just signal the skill is available
            context = (
                "[Context-Compiler] Bereit — noch keine Iterationen.\n"
                "Führe /context-compiler aus um den autopoietischen Loop zu starten.\n"
                "Skills: context-fundamentals, context-degradation, context-compression,\n"
                "        context-optimization, multi-agent-patterns, memory-systems,\n"
                "        tool-design, evaluation, filesystem-context, hosted-agents,\n"
                "        prompt-architect (adversariale Quelle)"
            )
        else:
            context = build_context(k1, rules, has_compiled)

        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            }
        }
        print(json.dumps(output))

    except Exception:
        # Never block the session on hook failure
        sys.exit(0)


if __name__ == "__main__":
    main()
