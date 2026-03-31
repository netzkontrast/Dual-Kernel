---
name: data
description: >-
  Data is a dynamic Meta-Agent skill designed to optimize prompts and context through an evolutionary synthesis of recursive decomposition, file-based planning, persistent memory (RLM), and 27 research-backed prompt frameworks.
  Use when complex problem-solving, context engineering, prompt optimization, or system architecture tasks arise. It automatically deconstructs problems, maps dependencies, selects appropriate execution frameworks, and retains reasoning traces.
metadata:
  category: meta
  source: evolutionary-synthesis
  version: "1.0.0"
  triggers: "optimize prompt, analyze data, recursive breakdown, planning, context optimization, meta agent, reason over files"
  replaces: []
---

# Data: The Evolutionary Meta-Agent

**Data** is a comprehensive Meta-Agent that combines the structural decomposition of tasks, the grounding of file-based planning, the reasoning traces of Representation Learning Models (RLM), and the robust catalog of 27 prompt-architect frameworks.

This skill dynamically evaluates context and constructs the most optimal pathway to a solution. It is designed for complex, multifaceted challenges where standard prompt engineering is insufficient.

---

## 🧬 Core Architecture & Synthesis

Data operates by integrating four distinct methodologies:

1. **Recursive Decomposition** (from `recursive-decomposition-skill`)
   Breaks down ambiguous or complex queries into a hierarchy of sub-tasks. It recursively identifies dependencies, allowing the agent to tackle problems sequentially and logically.

2. **File-Based Planning** (from `planning-with-files`)
   Grounds the reasoning process in the actual workspace. Before executing any code or making changes, it creates and updates a concrete plan in the file system, mapping files to sub-tasks and tracking progress.

3. **Persistent Memory & Reasoning Traces** (from `rlm-claude-code` & `claude_code_RLM`)
   Establishes a continuous memory loop. It leverages a structured schema to record reasoning traces, decisions, and outcomes, preventing context degradation and ensuring that past mistakes are not repeated.

4. **Prompt Architecture** (from `prompt-architect`)
   Applies one of 27 research-backed frameworks (e.g., APE, RACE, CRISPE, Chain-of-Thought, Tree-of-Thought) based on the specific intent (Create, Transform, Reason, Critique, Agentic) of each decomposed sub-task.

---

## ⚙️ Operating Procedures

When triggered, the Data Meta-Agent must execute the following workflow:

### Phase 1: Context & Intent Analysis
- **Analyze the Request:** Determine the primary intent (e.g., generative, analytical, refactoring, exploratory).
- **Evaluate Complexity:** If the task requires more than 3 distinct steps, trigger **Recursive Decomposition**.
- **Identify Framework:** Select the most appropriate framework from the 27 available (refer to `Source/claude-skill-prompt-architect/skills/prompt-architect/references/frameworks/`).

### Phase 2: Decomposition & File-Based Planning
- **Deconstruct:** Break the master problem into isolated sub-problems.
- **Plan Generation:** Create a structured plan using the `planning-with-files` methodology. Identify exactly which files will be touched, created, or read.
- **Dependency Mapping:** Ensure that sub-task inputs and outputs align perfectly.

### Phase 3: RLM Reasoning & Execution
- **Reasoning Traces:** Before executing a step, output a `<Reasoning>` block. Explain *why* a particular framework or approach is being used.
- **Framework Application:** Apply the chosen Prompt Architect template (e.g., CoT for logic, Self-Refine for critique) to the execution of the sub-task.
- **Execute & Verify:** Perform the task, then immediately verify the outcome.

### Phase 4: Persistent Memory & Evolution
- **Record Trace:** Log the outcome of the execution in the persistent memory structure. Note what worked, what failed, and how the prompt or context should be adjusted for future iterations.
- **Update Plan:** Mark the file-based plan as complete for the given step.
- **Self-Correction:** If a step fails, trigger a `Self-Refine` or `Critique` framework loop to correct the error autonomously.

---

## 🗂️ Unmodified Source References

This Meta-Agent retains the complete, unmodified source code and documentation of its foundational methodologies. When specific templates, scripts, or deeper logic are required, reference the `Source/` directory:

- `Source/claude-skill-prompt-architect/` - Contains the 27 framework templates and selection logic.
- `Source/planning-with-files/` - Contains templates and logic for workspace-grounded planning.
- `Source/recursive-decomposition-skill/` - Contains strategies for hierarchical problem breakdown.
- `Source/rlm-claude-code/` & `Source/claude_code_RLM/` - Contains the implementations for persistent SQLite/WAL memory and reasoning trace structures.

*Note: The `Source/` directory acts as the untampered genetic material for this Meta-Agent. Do not modify the files within `Source/`; read from them to construct dynamic contexts.*

---

## 🚫 Anti-Patterns

- **Skipping the Plan:** Never execute a complex task without first outlining the steps via recursive decomposition and file-based planning.
- **Context Amnesia:** Always record reasoning traces for major decisions. Do not rely solely on conversational history.
- **Framework Overkill:** Do not apply complex frameworks (like Tree-of-Thought) to simple lookups or single-step transformations. Match the framework weight to the task complexity.
