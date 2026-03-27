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


RECOVER_SIGNALS = {"reverse engineer", "recover prompt", "what prompt", "lost the prompt", "reconstruct"}
TRANSFORM_SIGNALS = {"rewrite", "refactor", "convert", "improve", "fix", "update", "change", "modify", "rework", "restructure"}
REASON_SIGNALS = {"calculate", "solve", "prove", "why does", "how does", "how many", "step by step", "explain why", "derive", "what percentage", "count"}
CRITIQUE_SIGNALS = {"review", "critique", "check", "verify", "validate", "assess", "audit", "stress test", "find flaws"}
CREATE_SIGNALS = {"create", "write", "generate", "build", "make", "add", "implement", "design", "draft", "produce"}

# Module-level constants for select_framework sub-classification (avoids per-call allocation)
_CRITIQUE_PRINCIPLE = {"principle", "standard", "rule", "policy"}
_CRITIQUE_FAILURE = {"fail", "risk", "wrong", "break", "worst"}
_TRANSFORM_REWRITE = {"rewrite", "convert", "restructure", "rework"}
_TRANSFORM_COMPRESS = {"compress", "shorten", "densif", "summar"}
_REASON_NUMERIC = {"number", "calculat", "percent", "how many", "total"}
_REASON_BRANCHING = {"multiple", "approach", "option", "way", "alternative"}
_CREATE_PROCEDURAL = {"step", "procedure", "process", "workflow", "pipeline", "phase"}
_CREATE_RULES = {"rule", "constraint", "must", "don't", "avoid", "never", "always", "comply"}
_CREATE_AUDIENCE = {"audience", "tone", "style", "voice", "brand", "reader"}
_CREATE_DATA = {"input", "transform", "output", "data", "format", "parse", "convert"}
_CREATE_ROLE = {"as a", "act as", "you are", "role", "persona", "expert"}

ALREADY_STRUCTURED_PATTERNS = re.compile(
    r"^(/|!)|"           # slash/bang commands
    r"(^[-*•]\s.+$)|"   # bulleted list
    r"(\d+\.\s.+$)|"    # numbered list
    r"(```)|"            # code block
    r"^(---|\*\*\w)",   # YAML or bold headers
    re.MULTILINE,
)


def detect_intent(prompt: str) -> str:
    p = prompt.lower()
    words = p.split()

    # CREATE takes priority if the prompt starts with a create verb (imperative commands)
    if words and any(words[0].startswith(s) for s in CREATE_SIGNALS):
        return "CREATE"

    if any(s in p for s in TRANSFORM_SIGNALS):
        return "TRANSFORM"
    if any(s in p for s in REASON_SIGNALS):
        return "REASON"
    if any(s in p for s in CRITIQUE_SIGNALS):
        return "CRITIQUE"
    if any(s in p for s in CREATE_SIGNALS):
        return "CREATE"
    if any(s in p for s in RECOVER_SIGNALS):
        return "RECOVER"
    if len(p) < 50:
        return "CLARIFY"

    return "CREATE"


def select_framework(intent: str, prompt: str) -> tuple[str, str]:
    """Return (framework_name, one_line_hint)."""
    p = prompt.lower()

    if intent == "RECOVER":
        return ("RPEF", "Analyze the output sample to reconstruct the original prompt.")

    if intent == "CLARIFY":
        return ("Reverse Role", "Prompt is underspecified — add: goal, context, output format, and constraints.")

    if intent == "CRITIQUE":
        if any(w in p for w in _CRITIQUE_PRINCIPLE):
            return ("CAI Critique-Revise", "State the principle to enforce, then critique and revise.")
        if any(w in p for w in _CRITIQUE_FAILURE):
            return ("Pre-Mortem", "Assume failure already happened — identify causes and warning signs.")
        return ("Self-Refine", "Specify quality dimensions and a stop condition.")

    if intent == "TRANSFORM":
        if any(w in p for w in _TRANSFORM_REWRITE):
            return ("BAB", "Specify: current state (Before), target state (After), transformation rules (Bridge).")
        if any(w in p for w in _TRANSFORM_COMPRESS):
            return ("Chain of Density", "Define iterations and compression target.")
        return ("Self-Refine", "Specify quality dimensions and stop condition for iterative improvement.")

    if intent == "REASON":
        if any(w in p for w in _REASON_NUMERIC):
            return ("Plan-and-Solve", "Extract all variables, plan the approach, then calculate.")
        if any(w in p for w in _REASON_BRANCHING):
            return ("Tree of Thought", "Explore distinct solution branches and compare by evaluation criteria.")
        return ("Chain of Thought", "Show reasoning steps explicitly with verification at each step.")

    # CREATE intent
    if any(w in p for w in _CREATE_PROCEDURAL):
        return ("RISEN", "Define: Role, Instructions, Steps, End goal, Narrowing (constraints).")
    if any(w in p for w in _CREATE_RULES):
        return ("TIDD-EC", "Separate Do/Don't lists with examples and context.")
    if any(w in p for w in _CREATE_AUDIENCE):
        return ("CO-STAR", "Specify: Context, Objective, Style, Tone, Audience, Response format.")
    if any(w in p for w in _CREATE_DATA):
        return ("RISE-IE", "Define input format, processing steps, and expected output structure.")
    if any(w in p for w in _CREATE_ROLE):
        return ("RACE", "Role + Action + Context + Expectation — make the outcome measurable.")
    if len(p) < 80:
        return ("RTF", "Add: Role (expertise), Task (exact action), Format (output structure).")

    return ("RISEN", "Structure as: Role, Instructions, Steps, End goal, Narrowing.")


def should_skip(prompt: str) -> bool:
    p = prompt.strip()

    if len(p.split()) <= 1:
        return True

    if ALREADY_STRUCTURED_PATTERNS.search(p):
        return True

    # Well-formed questions need no scaffolding
    if p.endswith("?") and len(p) > 60 and p[0].isupper():
        return True

    return False


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
