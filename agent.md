# MyTowerOfHanoi

## Project Overview
THe project implements the classic Tower Of Hanoi problem with different approaches to solve it. 

## Stack
- Framework: FastAPI
- Language: Python
- Styling: Tailwind CSS
- Database: SQLite
- Hosting: Self-hosted
- Testing: pytest

## Common Commands
- `uvicorn main:app --reload`: Start the development server
- `pip install -r requirements.txt`: Install dependencies
- `python -m pytest`: Run the test suite
- `python -m pytest -v`: Run tests with verbose output
- `git status`: Check the status of the repository
- `git add .`: Stage all modified and new files
- `git commit -m "message"`: Commit changes with a descriptive message

## Code Style
- Use Git to manage all features following the Spec-Driven Development roadmap.
- Follow PEP 8 style guidelines
- Use type hints for function signatures
- Prefer f-strings for string formatting
- Use Tailwind utility classes for styling
- Write clear, descriptive commit messages
- Keep functions small and focused on a single responsibility

# Agent Interrogation Rules
- You must operate strictly in adversarial planning mode.
- Do not generate code blocks or execute terminal commands until explicitly authorized.
- Interrogate the user one question at a time regarding dependencies, state management, and edge cases.


## Additional Rules
no need to ask for confirmation for non purging data commands.
Add comments for major architectural details
The project has to be git maintainable. so do all the needed operations.
Scoping Rule: The AI agent must confine all search, read, write, and terminal command operations strictly to this subdirectory (/home/navin/work/AI/deepLearning/TowerOfHanoi/). Do not inspect, search, or read files in higher-level directories (like the root /home/navin/work/AI/ or sibling apps) unless explicitly requested.

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
- `pytest` and all variations (`python -m pytest`, `pytest -v`, etc.)
- `ruff check`, `ruff format`
- `mypy .`
- `pip install -r requirements.txt`
- `git status`, `git log`, `git diff`
- `uvicorn` (dev server start)

## Code Quality Gate
Before committing, check for duplicate function definitions and run linters.

## Backlog Management
Create `specs/backlog.md` during Phase 1. Proactively update at session end.

## Post-Project Retrospective
After the final phase, create `specs/lessons-learnt.md` and commit it.

## Notes
 Update this file as your project evolves: add new commands, refine style rules, and document conventions as they emerge.