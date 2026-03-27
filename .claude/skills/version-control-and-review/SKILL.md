---
name: version-control-and-review
description: "Unified Git and code review skill. Covers committing with conventional format, pushing, PR creation, changelog generation, advanced Git workflows, and conducting or receiving code reviews."
risk: safe
source: self
tags: "[git, commit, PR, code-review, changelog, branch, push]"
date_added: "2026-03-27"
triggers: commit, push, PR, pull request, code review, git, branch, merge, rebase, cherry-pick, changelog, release notes, squash, history, stash
---

# Version Control & Code Review

Unified dispatcher for all Git, PR, and code review work.
Replaces: `git-advanced-workflows`, `git-pushing`, `commit`, `changelog-automation`, `create-pr`, `requesting-code-review`, `receiving-code-review`, `code-review-checklist`.

## Iron Law

```
NEVER commit directly to main or master without explicit user instruction.
ALWAYS use conventional commit format.
NEVER skip pre-commit hooks (--no-verify).
```

## ⚡ Decision Tree — What are you doing?

### 1. Committing changes

**Before every commit:**
```bash
git branch --show-current    # must NOT be main/master
git diff --staged            # review what will be committed
```

If on `main` / `master` → create a feature branch first.

**Conventional commit format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat` · `fix` · `docs` · `refactor` · `test` · `chore` · `perf` · `style` · `ci`

Rules:
- Subject: imperative mood, ≤72 chars, no period
- Body: explain *why*, not *what*; wrap at 100 chars
- Footer: reference issues (`Closes #123`), breaking changes (`BREAKING CHANGE:`)

```bash
git commit -m "$(cat <<'EOF'
feat(knowledge-graph): add entity extraction for Riss domain

Scans Markdown-docs/ for Riss mentions and generates entity files
with validated YAML frontmatter and wikilinks.

Closes #42
EOF
)"
```

### 2. Pushing to remote

```bash
git push -u origin <branch-name>
```

On failure: retry up to 4× with exponential backoff (2s, 4s, 8s, 16s). Do not force-push unless explicitly instructed.

Never force-push to `main` or `master`.

### 3. Creating a Pull Request

Use `gh pr create` with structured body:
```bash
gh pr create --title "<type>: brief description" --body "$(cat <<'EOF'
## Summary
- What changed and why

## Test plan
- [ ] Tests pass
- [ ] Linter clean
- [ ] Manual verification done
EOF
)"
```

PR title rules: ≤70 chars · conventional commit type prefix · no period.

### 4. Advanced Git workflows

**Clean history before merge:**
```bash
git rebase -i HEAD~N     # squash/fixup/reword commits
```

**Apply specific commits across branches:**
```bash
git cherry-pick <sha>    # apply single commit
```

**Find the commit that introduced a bug:**
```bash
git bisect start
git bisect bad           # current is broken
git bisect good <sha>    # last known good
# git bisect runs; test each step; git bisect good/bad
git bisect reset
```

**Recover from mistakes:**
```bash
git reflog               # find lost commits
git reset --soft HEAD~1  # undo last commit, keep changes staged
git restore --staged .   # unstage without losing edits
```

**Sync diverged branch:**
```bash
git fetch origin
git rebase origin/main   # prefer rebase over merge for feature branches
```

### 5. Changelog automation

Follow [Keep a Changelog](https://keepachangelog.com) format. Group entries under:
`Added` · `Changed` · `Deprecated` · `Removed` · `Fixed` · `Security`

Generate from commits:
```bash
git log --oneline <last-tag>..HEAD --pretty="format:- %s"
```

Tag releases with semver: `git tag -a v1.2.3 -m "Release v1.2.3"`

### 6. Conducting a code review

Evaluate in this order:
1. **Correctness** — does it do what was intended? edge cases?
2. **Security** — injection, auth bypass, data exposure, input validation
3. **Tests** — coverage, meaningful assertions, no brittle mocks
4. **Performance** — N+1 queries, unbounded loops, blocking I/O in hot paths
5. **Readability** — naming, complexity, unnecessary abstraction
6. **Architecture** — respects layer boundaries, no leaky abstractions

Comment conventions:
- `nit:` — minor style; author can ignore
- `suggestion:` — optional improvement
- `question:` — seeking understanding, not demanding change
- No prefix = blocking issue that must be resolved

### 7. Receiving a code review

- Read each comment fully before responding
- Don't argue; if you disagree, explain your reasoning with evidence
- For `nit:` comments: fix or explicitly decline with one sentence
- For blocking issues: fix, then re-request review
- Never take review comments personally — they are about the code

## Do not use this skill when
- You are only reading code with no intent to change or review it
- You need deployment or infrastructure pipeline changes (use CI/CD skill)
