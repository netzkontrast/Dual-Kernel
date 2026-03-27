# Hook Implementation Templates

Copy-paste Python starters for the two most common hook patterns.

---

## UserPromptSubmit — Context Injection

Runs before Claude sees the user's prompt. Use to suggest skills or inject context.

```python
#!/usr/bin/env python3
"""UserPromptSubmit hook — inject context into Claude's input."""
import json
import sys


SIGNALS = {"keyword1", "keyword2"}  # words that trigger this hook


def should_inject(prompt: str) -> bool:
    p = prompt.lower()
    return any(s in p for s in SIGNALS)


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
        prompt: str = data.get("prompt", "")

        if not prompt or len(prompt.split()) <= 3:
            sys.exit(0)

        if not should_inject(prompt):
            sys.exit(0)

        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "[Your message to Claude here]",
            }
        }
        print(json.dumps(output))

    except Exception:
        sys.exit(0)  # Never block the user on hook failure


if __name__ == "__main__":
    main()
```

**Register in settings.json:**
```json
"UserPromptSubmit": [
  {
    "type": "command",
    "command": "python3 /absolute/path/.claude/hooks/your-hook.py",
    "statusMessage": "Analyzing prompt..."
  }
]
```

---

## PreToolUse — Guardrail Block

Runs before Edit/Write/Bash executes. Exit code 2 blocks the tool and sends stderr to Claude.

```python
#!/usr/bin/env python3
"""PreToolUse hook — block tool execution if condition is met."""
import json
import sys


def should_block(data: dict) -> bool:
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    # --- detection logic here ---
    return False  # replace with real condition


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())

        if should_block(data):
            print(
                "BLOCKED — [reason]\n"
                "Required action:\n"
                "1. [Step 1]\n"
                "2. [Step 2]",
                file=sys.stderr,
            )
            sys.exit(2)  # exit 2 = block + send stderr to Claude

    except Exception:
        sys.exit(0)  # Fail open — never break Claude's workflow on hook error


if __name__ == "__main__":
    main()
```

**Register in settings.json (with tool matcher):**
```json
"PreToolUse": [
  {
    "matcher": "Edit|Write",
    "hooks": [
      {
        "type": "command",
        "command": "python3 /absolute/path/.claude/hooks/your-guard.py",
        "statusMessage": "Checking..."
      }
    ]
  }
]
```

---

## Exit Code Reference

| Exit code | Hook type | Effect |
|---|---|---|
| 0 | UserPromptSubmit | stdout → Claude's context |
| 0 | PreToolUse | Tool proceeds normally |
| 2 | PreToolUse | Tool blocked; stderr → Claude |
| other | any | Tool blocked; nothing sent to Claude |

Full I/O contract: [HOOK_MECHANISMS.md](HOOK_MECHANISMS.md)
