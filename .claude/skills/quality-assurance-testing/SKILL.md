---
name: quality-assurance-testing
description: "Unified QA skill covering TDD, systematic debugging, test fixing, Python testing, E2E/browser automation, linting, and verification. Use for any testing, debugging, or quality validation task."
risk: safe
source: self
tags: "[testing, tdd, debugging, pytest, playwright, e2e, lint, qa]"
date_added: "2026-03-27"
triggers: test, debug, bug, failure, TDD, pytest, playwright, selenium, E2E, lint, validate, fix tests, broken tests, test suite, flaky, assertion, mock, fixture, coverage, ruff, mypy, tsc
---

# Quality Assurance & Testing

Unified dispatcher for all testing, debugging, and quality validation work.
Replaces: `systematic-debugging`, `test-fixing`, `test-driven-development`, `e2e-testing-patterns`, `python-testing-patterns`, `browser-automation`, `lint-and-validate`, `verification-before-completion`.

## Iron Laws (non-negotiable)

```
1. NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST  (TDD)
2. NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST  (debugging)
3. NO TASK IS "DONE" WITHOUT RUNNING VALIDATORS     (lint/validate)
```

Violating these is violating the spirit of quality engineering.

## ⚡ Decision Tree — What phase are you in?

### Phase 1: Writing new code (TDD)
**Always write the test first. Watch it fail. Write minimal code to pass.**

```
Red → Green → Refactor
```

1. Write a failing test that defines desired behavior
2. Confirm it fails (if it passes without code, the test is wrong)
3. Write the minimum code to make it pass
4. Refactor with tests green

Exceptions (check with human): throwaway prototypes · generated code · configuration files.

**Python TDD stack:** `pytest` · `pytest-asyncio` · `factory_boy` · `Faker` · `unittest.mock`

```python
# Test first, then implement
def test_order_cannot_be_submitted_empty():
    order = Order()
    with pytest.raises(ValueError, match="empty"):
        order.submit(items=[])
```

### Phase 2: Debugging a bug or unexpected behavior
**Rule: FIND ROOT CAUSE before proposing any fix.**

Investigation protocol:
1. **Reproduce** — get a minimal reproduction case; confirm the bug is real
2. **Isolate** — narrow scope: which module, which input, which code path?
3. **Hypothesize** — form one specific hypothesis about root cause
4. **Verify** — add a targeted assertion or log to confirm/deny
5. **Fix** — change only what the root cause demands
6. **Regression test** — add a test that would have caught this bug

Do not: guess and patch · apply multiple fixes simultaneously · skip reproduction · ignore the stack trace.

### Phase 3: Fixing failing tests
When the test suite is broken:
1. Run the full suite; capture all failures
2. Group failures by pattern (shared fixture? import error? mock mismatch?)
3. Fix the highest-leverage root cause first (often one fix clears many failures)
4. Re-run after each fix; never batch multiple fixes before verifying
5. Never delete a failing test unless it tests behavior that was intentionally removed

### Phase 4: E2E / Browser automation
Use **Playwright** as the default (over Selenium / Puppeteer) for new projects.

```python
from playwright.async_api import async_playwright

async def test_login_flow(page):
    await page.goto("/login")
    await page.fill('[name="email"]', "user@example.com")
    await page.fill('[name="password"]', "secret")
    await page.click('[type="submit"]')
    await expect(page.locator("h1")).to_contain_text("Dashboard")
```

Rules for resilient selectors (prefer in order):
1. `data-testid` attributes
2. ARIA roles (`get_by_role`)
3. Text content (`get_by_text`)
4. CSS classes (last resort)

Flakiness prevention: use `expect()` assertions (auto-retry) · never `time.sleep()` · mock external APIs · seed deterministic test data.

### Phase 5: Lint and validate (MANDATORY after every change)

**Run after EVERY code change. Do not mark a task done without clean validators.**

#### Python
```bash
ruff check . --fix          # lint + autofix
mypy .                       # type checking
bandit -r . -ll              # security scan
python -m pytest             # run tests
```

#### Node.js / TypeScript
```bash
npm run lint                 # ESLint
npx tsc --noEmit             # TypeScript types
npm audit --audit-level=high # security
npm test                     # tests
```

#### This project (Kohärenz Protokoll)
```bash
source .venv/bin/activate
python tools/frontmatter_validator.py knowledge-graph/
python tools/wikilink_checker.py knowledge-graph/
python tools/consistency_checker.py knowledge-graph/
```

### Phase 6: Verifying completion
**Do not claim a task is "done" until:**
- [ ] All relevant tests pass
- [ ] Linter reports zero errors
- [ ] Type checker passes
- [ ] The behavior was manually verified against the original requirement
- [ ] Edge cases were considered and either tested or explicitly scoped out

## Do not use this skill when
- You need to write exploratory throwaway code with no quality requirements
- You are only doing documentation edits with no code changes
