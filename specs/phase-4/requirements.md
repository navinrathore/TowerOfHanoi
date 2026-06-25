# Phase 4 Requirements — Interactive Web UI (Playable Mode)

## Scope

Define and implement the visual interactive user interface for the Tower of Hanoi application. This includes creating a responsive dashboard styled with a dark slate and neon violet theme, setting up Jinja2 rendering templates, configuring FastAPI backend routes to save game runs in batches, and implementing click-to-move and drag-and-drop gameplay support.

1. **Backend Integration**:
   - Serve static javascript and css assets via FastAPI `StaticFiles`.
   - Setup a `Jinja2Templates` instance pointing to the templates directory.
   - HTML Router `/` rendering the game dashboard, pre-populated with recent database runs.
   - Pydantic models to parse a complete game run session, including multiple individual moves, in a single transaction payload.
   - Endpoint `POST /api/runs` to create, persist, and complete a game run with its moves.
   - Endpoint `GET /api/runs` to list the 10 most recent runs.

2. **Frontend UI/UX**:
   - Layout template `base.html` configured with Google Font "Outfit" and Tailwind CSS CDN.
   - Play space container displaying 3 vertical rods on a shared wooden platform base.
   - Colorful, pill-shaped disks dynamically sized based on their disk numbers.
   - Stats meters tracking elapsed time (stopwatch), move counter, optimal move boundary ($2^n - 1$), and movement efficiency score.
   - Control triggers to select disk size (3 to 8 disks) and start a new game session.
   - Celebratory win card overlay shown when all disks reach Peg C.

3. **Game Mechanics**:
   - **Click-to-Move**: Click a rod to select the top disk, then click a target rod to move it.
   - **Drag-and-Drop**: Standard HTML5 drag-and-drop support on top disks.
   - Move validation preventing larger disks from stacking on top of smaller ones.
   - Interactive feedback toasts and shake animations on invalid placements.

4. **Testing**:
   - Integration tests in `tests/test_api.py` verifying HTML routing, batch run submissions, payload validation error codes, and sorting of retrieved runs.
   - SQLite `StaticPool` configuration to maintain schema consistency across test threads.

## Out of Scope

- Algorithmic solvers generating movements automatically (Phase 5).
- Heuristic-based A* path solvers (Phase 6).
- Reinforcement learning training dashboard and analytics visualizations (Phase 7).

## Design Decisions

- **Batch Logging**: To simplify HTTP operations and database transaction locks, all move details and game metadata are sent in a single transaction payload upon winning, rather than sending a POST on every click.
- **Tailwind CDN**: A CDN link prevents complex local frontend build pipelines while maintaining quick rendering and rich visual utility options.
