#!/usr/bin/env python3
"""UserPromptSubmit hook: auto-apply prompt-architect framework hints.

Reads JSON from stdin (Claude Code UserPromptSubmit event),
detects intent, selects appropriate framework, and injects
additionalContext to guide Claude's response structure.

Skips: slash commands, already-structured prompts, very short queries.
"""
import json
import re
import sys


# ---------------------------------------------------------------------------
# Intent detection
# ---------------------------------------------------------------------------

RECOVER_SIGNALS = {"reverse engineer", "recover prompt", "what prompt", "lost the prompt", "reconstruct"}
TRANSFORM_SIGNALS = {"rewrite", "refactor", "convert", "improve", "fix", "update", "change", "modify", "rework", "restructure"}
REASON_SIGNALS = {"calculate", "solve", "prove", "why does", "how does", "how many", "step by step", "explain why", "derive", "what percentage", "count"}
CRITIQUE_SIGNALS = {"review", "critique", "check", "verify", "validate", "assess", "audit", "stress test", "find flaws"}
CREATE_SIGNALS = {"create", "write", "generate", "build", "make", "add", "implement", "design", "draft", "produce"}


def detect_intent(prompt: str) -> str:
    p = prompt.lower()
    words = p.split()

    if any(s in p for s in RECOVER_SIGNALS):
        return "RECOVER"

    # CREATE takes priority if the prompt *starts* with a create verb
    if words and any(words[0].startswith(s) for s in CREATE_SIGNALS):
        return "CREATE"

    if any(s in p for s in TRANSFORM_SIGNALS):
        return "TRANSFORM"
    if any(s in p for s in CRITIQUE_SIGNALS):
        return "CRITIQUE"
    if any(s in p for s in REASON_SIGNALS):
        return "REASON"
    if any(s in p for s in CREATE_SIGNALS):
        return "CREATE"
    if len(prompt.strip()) < 50:
        return "CLARIFY"

    return "CREATE"


# ---------------------------------------------------------------------------
# Framework selection
# ---------------------------------------------------------------------------

def select_framework(intent: str, prompt: str) -> tuple[str, str]:
    """Return (framework_name, one_line_hint)."""
    p = prompt.lower()

    if intent == "RECOVER":
        return ("RPEF", "Analyze the output sample to reconstruct the original prompt.")

    if intent == "CLARIFY":
        return ("Reverse Role", "Prompt is underspecified — add: goal, context, output format, and constraints.")

    if intent == "CRITIQUE":
        if any(w in p for w in ["principle", "standard", "rule", "policy"]):
            return ("CAI Critique-Revise", "State the principle to enforce, then critique and revise.")
        if any(w in p for w in ["fail", "risk", "wrong", "break", "worst"]):
            return ("Pre-Mortem", "Assume failure already happened — identify causes and warning signs.")
        return ("Self-Refine", "Specify quality dimensions and a stop condition.")

    if intent == "TRANSFORM":
        if any(w in p for w in ["rewrite", "convert", "restructure", "rework"]):
            return ("BAB", "Specify: current state (Before), target state (After), transformation rules (Bridge).")
        if any(w in p for w in ["compress", "shorten", "densif", "summar"]):
            return ("Chain of Density", "Define iterations and compression target.")
        return ("Self-Refine", "Specify quality dimensions and stop condition for iterative improvement.")

    if intent == "REASON":
        if any(w in p for w in ["number", "calculat", "percent", "how many", "total"]):
            return ("Plan-and-Solve", "Extract all variables, plan the approach, then calculate.")
        if any(w in p for w in ["multiple", "approach", "option", "way", "alternative"]):
            return ("Tree of Thought", "Explore distinct solution branches and compare by evaluation criteria.")
        return ("Chain of Thought", "Show reasoning steps explicitly with verification at each step.")

    # CREATE intent
    if any(w in p for w in ["step", "procedure", "process", "workflow", "pipeline", "phase"]):
        return ("RISEN", "Define: Role, Instructions, Steps, End goal, Narrowing (constraints).")
    if any(w in p for w in ["rule", "constraint", "must", "don't", "avoid", "never", "always", "comply"]):
        return ("TIDD-EC", "Separate Do/Don't lists with examples and context.")
    if any(w in p for w in ["audience", "tone", "style", "voice", "brand", "reader"]):
        return ("CO-STAR", "Specify: Context, Objective, Style, Tone, Audience, Response format.")
    if any(w in p for w in ["input", "transform", "output", "data", "format", "parse", "convert"]):
        return ("RISE-IE", "Define input format, processing steps, and expected output structure.")
    if any(w in p for w in ["as a", "act as", "you are", "role", "persona", "expert"]):
        return ("RACE", "Role + Action + Context + Expectation — make the outcome measurable.")
    if len(prompt.strip()) < 80:
        return ("RTF", "Add: Role (expertise), Task (exact action), Format (output structure).")

    return ("RISEN", "Structure as: Role, Instructions, Steps, End goal, Narrowing.")


# ---------------------------------------------------------------------------
# Skip conditions
# ---------------------------------------------------------------------------

ALREADY_STRUCTURED_PATTERNS = re.compile(
    r"^(/|!)|"           # slash commands, bang commands
    r"(^[-*•]\s.+$)|"   # bulleted list
    r"(\d+\.\s.+$)|"    # numbered list
    r"(```)|"            # code block
    r"^(---|\*\*\w)",   # YAML or bold headers
    re.MULTILINE,
)


def should_skip(prompt: str) -> bool:
    p = prompt.strip()

    # Slash commands and bang commands
    if p.startswith("/") or p.startswith("!"):
        return True

    # Single word or emoji
    if len(p.split()) <= 1:
        return True

    # Already has structural markers
    if ALREADY_STRUCTURED_PATTERNS.search(p):
        return True

    # Pure questions that are well-formed (contains "?" and is >40 chars)
    if p.endswith("?") and len(p) > 60 and p[0].isupper():
        return True

    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
        prompt: str = data.get("prompt", "")

        if not prompt or should_skip(prompt):
            sys.exit(0)

        intent = detect_intent(prompt)
        framework, hint = select_framework(intent, prompt)

        context = (
            f"[Prompt-Architect] Intent: {intent} → Framework: {framework}\n"
            f"Suggestion: {hint}\n"
            f"Apply this structure to your response if the user hasn't already specified a format."
        )

        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context,
            }
        }
        print(json.dumps(output))

    except Exception:
        # Never block the user's prompt on hook failure
        sys.exit(0)


if __name__ == "__main__":
    main()
