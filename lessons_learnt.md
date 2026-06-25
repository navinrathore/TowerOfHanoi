# Lessons Learnt — TowerOfHanoi SDD Project

**Project**: MyTowerOfHanoi  
**Date**: 2026-06-25  
**Methodology**: Spec-Driven Development (SDD) across 9 phases, 8 agent sessions  

---

## Summary

14 lessons identified across 6 categories. Each lesson includes the observed problem, evidence, root cause analysis, and a recommended fix with **placement guidance** for where the rule should live.

### Placement Key

| Tag | Meaning |
|-----|---------|
| 🌍 `GLOBAL` | Add to `AI_INSTRUCTIONS.md` (applies to all projects in the workspace) |
| 📁 `PROJECT` | Add to project-level `agent.md` (project-specific) |
| 🧠 `BEHAVIOUR` | Agent should internalise this — no file change needed, but worth documenting |

---

## Category 1: SDD Process Discipline

### L01. Roadmap status not auto-updated after phase completion

**What happened**: After completing Phases 3, 4, and 5, the `roadmap.md` file was NOT updated with `(Completed)` status. The user had to explicitly ask: *"again roadmap files is not updated for phase 3 and 4 status"* (Phase 5 session). The roadmap was only bulk-updated at the very end (commit `aa25f77`).

**Root cause**: No rule mandating automatic roadmap status updates as part of the phase completion checklist.

> [!IMPORTANT]
> **Fix** 📁 `PROJECT` — Add to `agent.md`:
> ```markdown
> ## SDD Phase Completion Checklist
> After completing each phase, the agent MUST:
> 1. Update `specs/roadmap.md` — mark the phase as `(Completed)`
> 2. Run the full test suite (`pytest`)
> 3. Commit all changed files with a descriptive message
> 4. Suggest the prompt for the next phase
> ```

---

### L02. Phase spec files not consistently created

**What happened**: Phase 4 initially had no spec files (requirements.md, plan.md, validation.md). The user noticed and asked: *"in phase 4, no spec files are created. is that by plan or something else?"* Similarly, Phase 5 initially launched without specs until the user flagged it: *"seems for phase 5 also you did not make the spec files."*

Phases 6–9 had specs created in the same commit as the implementation, meaning specs were written concurrently rather than before coding — violating the "spec-driven" principle.

**Root cause**: No explicit SDD rule requiring spec files to be written **before** implementation begins.

> [!IMPORTANT]
> **Fix** 📁 `PROJECT` — Add to `agent.md`:
> ```markdown
> ## SDD Spec-First Rule
> For EVERY phase, the agent MUST create `specs/phase-N/` with:
> - `requirements.md` — what to build
> - `plan.md` — how to build it
> - `validation.md` — how to verify it
> These files MUST be committed BEFORE implementation code is written.
> ```

---

### L03. Backlog file not created proactively

**What happened**: The `backlog.md` file was not part of the initial project scaffolding. It was created later during Phase 3 (commit `8929ec6`), and then had to be prompted for updates: *"Do you want to add anything from current session into backlog file?"* was asked by the user across 4 separate sessions.

**Root cause**: No rule to create a backlog file during initial scaffolding, or to auto-update it at session end.

> [!IMPORTANT]
> **Fix** 📁 `PROJECT` — Add to `agent.md`:
> ```markdown
> ## Backlog Management
> - A `specs/backlog.md` file MUST be created during Phase 1 scaffolding.
> - At the end of each session, the agent SHOULD proactively review whether any
>   discoveries, deferred items, or nice-to-haves should be added to the backlog.
>   Do not wait for the user to ask.
> ```

---

### L04. No lessons learnt / retrospective process built into SDD

**What happened**: The user had to explicitly request this document at the very end. An iterative lessons learnt process would have caught issues like L01–L03 much earlier.

**Root cause**: SDD methodology as defined didn't include a retrospective step.

> [!TIP]
> **Fix** 📁 `PROJECT` — Add to `agent.md`:
> ```markdown
> ## Post-Implementation Retrospective
> After the final phase is complete, the agent MUST create a `specs/lessons-learnt.md`
> file documenting process issues, code quality findings, and improvement suggestions.
> This file should be committed to the repo so future projects can reference it.
> ```

---

## Category 2: Git & DevOps

### L05. Git repo not initialized automatically

**What happened**: The user had to explicitly instruct: *"The git repo is not initialized yet. You may have to make it."* during Phase 1. The agent didn't check for or create a git repository as part of project scaffolding.

**Root cause**: No scaffolding checklist that includes git initialization.

> [!WARNING]
> **Fix** 📁 `PROJECT` — Add to `agent.md`:
> ```markdown
> ## Git Setup (New Projects)
> During Phase 1 scaffolding, the agent MUST:
> 1. Check if a git repo exists (`git status`)
> 2. If not, run `git init` and create a `.gitignore`
> 3. Add git commands to the Common Commands section of agent.md
> ```

---

### L06. Files not committed at phase completion

**What happened**: In Phase 2, the user asked: *"Why the files are not committed?"* In Phase 4, they explicitly flagged: *"the files are not committed of this phase?"* The agent completed implementation and tests but left uncommitted changes.

**Root cause**: Git commit was not part of the mandatory phase completion flow.

> [!WARNING]
> **Fix** 📁 `PROJECT` — Already addressed by the checklist in L01. The key rule:
> ```markdown
> ## Git Commit Rule
> All modified and new files MUST be committed with a descriptive message before
> declaring a phase complete. Use: `git add . && git commit -m "phase description"`
> ```

---

## Category 3: Agent Behaviour & Context

### L07. Agent browsed files outside project subdirectory

**What happened**: The user noticed the agent was reading `AI_INSTRUCTIONS.md` from a parent directory and asked: *"Why are you looking for AI_instructions.md file? How would you know which subdirectory to work upon?"* This led to adding the scoping rule in `agent.md` (commit `7e978e1`).

**Root cause**: No subdirectory scoping rule. The agent's knowledge item pointed to a global `AI_INSTRUCTIONS.md` which caused it to search upward.

> [!IMPORTANT]
> **Fix** 📁 `PROJECT` — Already added to `agent.md`:
> ```markdown
> ## Scoping Rule
> The AI agent must confine all search, read, write, and terminal command operations
> strictly to this subdirectory. Do not inspect, search, or read files in higher-level
> directories unless explicitly requested.
> ```
> ✅ This was correctly identified and fixed during the project. Include it in **all future project** `agent.md` files from the start.

---

### L08. Agent asked for confirmation on non-destructive commands

**What happened**: The user was frustrated by permission prompts for `pytest`, `ruff`, `mypy`, and `pip install -r requirements.txt`. These are safe, read-only or local-install commands that should not require explicit approval.

**Root cause**: Default security posture treats all commands equally.

> [!TIP]
> **Fix** 📁 `PROJECT` — Already partially in `agent.md`:
> ```markdown
> ## Additional Rules
> No need to ask for confirmation for non-purging data commands.
> ```
> **Strengthen** to be more explicit:
> ```markdown
> ## Pre-Approved Commands (no confirmation needed)
> - `pytest` and all variations (`python -m pytest`, `pytest -v`, etc.)
> - `ruff check`, `ruff format`
> - `mypy .`
> - `pip install -r requirements.txt`
> - `git status`, `git log`, `git diff`
> - `uvicorn` (dev server start)
> ```

---

### L09. `/grill-me` not leveraged early enough

**What happened**: The user used `/grill-me` during Phase 4, which produced a useful design interview. However, this was reactive rather than proactive. For a project like this with UI, database, and RL components, an early design interview would have prevented ambiguity.

**Root cause**: The agent didn't proactively suggest `/grill-me` for complex phases.

> [!TIP]
> **Fix** 🧠 `BEHAVIOUR` — Agent should suggest `/grill-me` when:
> - A phase involves **user-facing UI** decisions (layout, interaction model)
> - A phase introduces a **new architectural layer** (database, ML, API)
> - Requirements are ambiguous or have multiple valid interpretations
> 
> Consider adding to `agent.md`:
> ```markdown
> ## Design Interrogation
> For phases involving UI, architecture, or ambiguous requirements, the agent SHOULD
> suggest `/grill-me` before creating the implementation plan.
> ```

---

## Category 4: Session Management

### L10. New session context bootstrapping was manual

**What happened**: The user had to carefully craft prompts for each new session, e.g.: *"We have completed Phase 1 of MyTowerOfHanoi under specs/ and agent.md. Let's write the specifications for Phase 2 next."* Without this explicit context, the agent might not know what phase to work on.

**Root cause**: No standardised "session handoff" protocol.

> [!TIP]
> **Fix** 📁 `PROJECT` — Add to `agent.md`:
> ```markdown
> ## New Session Bootstrap
> At the start of every new session, the agent MUST:
> 1. Read `agent.md` for project context
> 2. Read `specs/roadmap.md` to identify completed vs pending phases
> 3. Check `git log -5` for recent work
> 4. Run `pytest` to confirm test baseline
> 5. Identify the next incomplete phase and confirm with the user
> ```

---

### L11. Combining multiple phases in one session created quality gaps

**What happened**: Phases 6+7 were implemented together (commit `1da10bf`), and Phases 8+9 were combined (commit `e4dd1c1`). While this was efficient, it led to the spec files being created alongside code rather than beforehand, violating SDD principles.

**Root cause**: Time pressure or user request to batch phases. No guard-rail in agent.md.

> [!TIP]
> **Fix** 🧠 `BEHAVIOUR`:
> ```markdown
> ## Phase Batching Warning
> If the user requests multiple phases in one session, the agent SHOULD:
> 1. Warn that SDD best practice is one phase per session
> 2. If proceeding, still create spec files BEFORE implementation for each phase
> 3. Commit each phase separately (not in a single monolithic commit)
> ```

---

## Category 5: Code Quality

### L12. Duplicate function definitions in crud.py

**What happened**: Six CRUD functions (`create_game_run`, `add_game_move`, `complete_game_run`, `get_game_run`, `get_all_game_runs`, `get_game_moves`) were defined twice in `crud.py` — lines 10–150 and again at lines 345–486. Python silently uses the last definition, so this didn't cause runtime errors but was 144 lines of dead code.

**Root cause**: Likely a merge/append issue when multiple phases edited the same file across sessions without checking for existing definitions.

> [!WARNING]
> **Fix** 🧠 `BEHAVIOUR`:
> - Before adding functions to an existing file, **grep for the function name** first
> - After implementation, run a quick duplicate check: `grep -n "^def " file.py | sort`
> - Consider adding a linting step to `agent.md`:
> ```markdown
> ## Code Quality Checks
> Before committing, verify:
> - No duplicate function/class definitions: `grep -c "^def func_name" file.py`
> - `ruff check .` passes
> - `mypy .` passes (if configured)
> ```

---

### L13. Seed data function bypasses validation

**What happened**: The `seed_database_if_empty()` function in `crud.py` directly creates `models.GameRun` objects without going through the validated `create_game_run()` function. While acceptable for seeding, this pattern can mask schema changes.

**Root cause**: Expedient seeding during rapid development.

> [!TIP]
> **Fix** 🧠 `BEHAVIOUR` — Low priority. Consider using the CRUD layer even for seed data to maintain consistency. Document the decision if bypassing.

---

## Category 6: Review & Verification Process

### L14. No reviewer checklist existed

**What happened**: The user asked *"As a review, what do I need to check? Make a plan for reviewer."* There was no standard review template.

> [!IMPORTANT]
> **Fix** 📁 `PROJECT` — Create a reviewer checklist template:
> ```markdown
> ## Reviewer Checklist (Per Phase)
> - [ ] Spec files exist in `specs/phase-N/` (requirements, plan, validation)
> - [ ] `roadmap.md` status updated to `(Completed)`
> - [ ] All tests pass (`pytest -v`)
> - [ ] Static analysis clean (`ruff check .`, `mypy .`)
> - [ ] All files committed (`git status` is clean)
> - [ ] No duplicate code or dead code introduced
> - [ ] Backlog updated with deferred items
> - [ ] Code comments explain architectural decisions
> ```

---

## Recommended `agent.md` Additions

Below is a consolidated block that can be appended to the project's `agent.md` to prevent recurrence of these issues. It covers L01–L14:

```markdown
<!-- SDD LESSONS LEARNT RULES — Added from TowerOfHanoi retrospective -->

## SDD Phase Completion Checklist
After completing each phase, the agent MUST:
1. Create/verify spec files exist: `specs/phase-N/{requirements,plan,validation}.md`
2. Update `specs/roadmap.md` — mark the phase as `(Completed)`
3. Run the full test suite (`python -m pytest -v`)
4. Run static analysis (`ruff check .`)
5. Commit ALL changed files (`git add . && git commit`)
6. Review and update `specs/backlog.md` with deferred items
7. Suggest the prompt for the next phase/session

## SDD Spec-First Rule
Spec files (requirements, plan, validation) MUST be written and committed
BEFORE implementation code. Never create specs alongside or after code.

## Git Setup (New Projects)
During initial scaffolding, verify git is initialized. If not, run `git init`,
create `.gitignore`, and make an initial commit.

## New Session Bootstrap
At session start: read `agent.md`, check `specs/roadmap.md`, run `git log -5`,
run `pytest`, and identify the next phase.

## Pre-Approved Commands (no confirmation needed)
pytest, ruff, mypy, pip install -r requirements.txt, git status/log/diff,
uvicorn (dev server).

## Code Quality Gate
Before committing, check for duplicate function definitions and run linters.

## Backlog Management
Create `specs/backlog.md` during Phase 1. Proactively update at session end.

## Post-Project Retrospective
After the final phase, create `specs/lessons-learnt.md` and commit it.
```

---

## Items NOT Lessons (Acknowledged)

| User Note | Assessment |
|---|---|
| *"backlog — nothing to do as of now"* | ✅ Correct — backlog items are future scope, not defects |
| *"pip install requirements.txt — no permission required"* | ✅ Covered by L08 |
| *"starting a new session for Phase 2 is prudent"* | ✅ Correct — SDD best practice confirmed |
| *"Phase 2: pytest passes with existing test cases — why?"* | ✅ Expected — running existing tests as a sanity check ensures no regressions. This is good practice, not an issue |
