# Phase 4 Plan — Interactive Web UI (Playable Mode)

This document outlines the step-by-step implementation plan for building the interactive playable dashboard.

---

## Group 1 — Dependency Setup

1. Add `jinja2==3.1.4` to `requirements.txt`.
2. Run `pip install -r requirements.txt` to sync the environment.

## Group 2 — Backend Routing & API

3. Mount static directory at `/static` and templates directory at `/templates` in `main.py`.
4. Define Pydantic request and response schemas in `main.py`:
   - `MoveSchema` validation schema for moves.
   - `GameRunBatchCreate` transaction container.
   - `GameMoveResponse` and `GameRunResponse` serializing models using modern `model_config = ConfigDict(from_attributes=True)`.
5. Implement endpoints:
   - `GET /` to render the dashboard, pre-populated with database runs.
   - `POST /api/runs` to atomic-commit a completed game run with all moves.
   - `GET /api/runs` to retrieve recent game runs.

## Group 3 — Base Layout Styling

6. Create `templates/base.html` template layout with:
   - Google Font (Outfit).
   - Tailwind CSS CDN.
   - Dark Slate & Indigo neon aesthetic styling definitions.
7. Create `static/css/styles.css` with animation properties:
   - Disk translation transitions.
   - Neon pulsing outline for selected disks (`selected-disk-glow`).
   - Shake keyframes for invalid moves.
   - Customized dark scrollbars.

## Group 4 — Web Dashboard Template

8. Create `templates/index.html` structure extending `base.html`:
   - Settings control bar (disk selection, new game, reset).
   - Dynamic gameplay counters (timer, move count, efficiency status).
   - Visualization board showing three rods on a platform.
   - Victory message overlay card.
   - Leaderboard panel.

## Group 5 — Client Application Logic

9. Create `static/js/game.js` implementing client gameplay:
   - Track local stacks, timer intervals, and move log lists.
   - Render rods and sized gradient disks.
   - Hook **Click-to-Move** select/destination handlers.
   - Hook **Drag-and-Drop** `dragstart`/`dragover`/`drop` event listeners.
   - Save victory stats to `POST /api/runs` and update leaderboard.

## Group 6 — Verification Tests

10. Create `tests/test_api.py` testing routers, boundary limits, and database operations.
11. Update `tests/test_main.py` root route checks to validate HTML dashboard layouts.
12. Run formatting, lint checks, type checks, and pytests to verify correctness.
