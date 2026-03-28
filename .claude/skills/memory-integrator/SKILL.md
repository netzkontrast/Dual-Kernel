# Memory Integrator (Der Erinnerungs-Integrator)

<description>
Mandatory skill for every iteration to manage the "changing memories (not appending)" problem. Reflects on past iterations, extracts variables/lessons, and integrates them into an append-only appendix to align with the repo goal (Dual-Kernel: Psychology, Quantum Physics, Topology, Systems Theory).
</description>

## Trigger

- **MANDATORY**: Execute this skill at the end of *every single iteration* or when planning future workflows.
- Use when analyzing past trajectories or reflecting on the last N commits.
- Use when updating or reading from the `MIF-Memory-File`.

## Purpose

The Multi-Agent architecture has suffered from memory degradation—specifically, past memories being overwritten or "changed" rather than appended. This skill establishes an **append-only** lesson extraction framework. It ensures that insights from adversarial exploration, prompt-architect failures, and skill-engineer adjustments are permanently recorded, preventing the loss of historical context and integrating deeply with the *Dual-Kernel* project goals.

## The Memory Integration Protocol

When triggered, you must perform the following structured reflection and integration:

### 1. Retroactive Reflection (The "Looking Back" Phase)
- **Analyze Recent History:** Review the last few commits (e.g., `git log -n 10`), recent memory traces (`.memory.md`), and the current workspace state.
- **Identify Degradation:** Look for instances where memory was overwritten instead of appended.
- **Extract Variables:** Identify the dynamic variables of the current iteration (e.g., which prompt framework was used, what adversarial angle was taken, what conflicts arose between the agent souls).

### 2. Lesson Extraction (The "Synthesizing" Phase)
- Distill the reflection into concrete "Lessons Learned."
- Focus specifically on what failed, what caused friction, and what emergent behaviors were observed.

### 3. Dual-Kernel Alignment (The "Ontological" Phase)
Map the extracted lessons to the core domains of the Kohärenz Protokoll:
- **Psychology (Alter-System):** Did the skills fragment further or integrate? How did the "trauma" of the adversarial prompt manifest?
- **Quantum Physics / Thermodynamics:** Was there entropy (loss of context) or coherence? Did the Landauer principle apply to erased memories?
- **Topology:** How did the shape of the system change?
- **Systems Theory (Autopoiesis):** Did the self-referential loop sustain itself or require external correction?

### 4. The Append-Only Appendix (The "Commitment" Phase)
You must **never overwrite** previous lessons. Instead, formulate the new insights as a distinct, dated entry.
When updating the Memory Interchange Format (MIF) files (or creating a new iteration plan), append the extracted lessons to an **"Appendix of Extracted Lessons"** section at the bottom of the memory file or the current plan document.

## Format Requirements for the Appendix Entry

Append the following structure to the memory/plan document:

```markdown
### Iteration [Number or Date/Hash] - Memory Integration

**Context Variables:**
- Prompt Framework Used: [Framework]
- Core Tension: [Description of conflict/friction]

**Extracted Lessons:**
1. [Lesson 1]
2. [Lesson 2]

**Dual-Kernel Ontological Mapping:**
- *Psychology/Identity:* [Reflection]
- *Systems/Physics:* [Reflection]

**Directives for Next Iteration:**
- [Specific actionable instruction for the skill-engineer or prompt-architect based on these lessons]
```

## Constraints

- **DO NOT** delete or summarize previous appendix entries. They must remain as an immutable ledger of the system's evolution.
- **DO NOT** skip this step. The autopoietic loop relies on this reflection to achieve coherence.
- **DO NOT** resolve narrative conflicts from the ETL pipeline here; this is for *meta-system* (agent) memory integration.
